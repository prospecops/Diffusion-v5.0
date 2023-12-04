import json, logging
import html
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from depots.models import Depot
from .forms import BulkCTMForm, IndividualCTMForm
from .models import BulkCTM, CTMInventory, TemporaryCTMInventory
from .models import IndividualCTM  # Import your IndividualCTM model

from datetime import datetime
import re
from .models import CTMInventory


@login_required
@permission_required('supplier.view_supplier_portal', raise_exception=True)
def depot_inventory_shipments(request):
    # Query for Individual CTMs with kits
    ctms_with_kits = (IndividualCTM.objects
                      .values('ctm_name', 'kit_serial_number', 'lot_number', 'quantity', 'expiration_date')
                      .filter(kit_serial_number__isnull=False)
                      .distinct()
                      .order_by('ctm_name', 'kit_serial_number'))

    # Get distinct Individual CTM names for the dropdown
    unique_individual_ctm_names = IndividualCTM.objects.order_by('ctm_name').values_list('ctm_name',
                                                                                         flat=True).distinct()

    # Serialize the data for Individual CTMs
    ctms_with_kits_json = mark_safe(json.dumps(list(ctms_with_kits), cls=DjangoJSONEncoder))

    # Query for all Bulk CTMs
    bulk_ctms = (BulkCTM.objects
                 .values('ctm_name', 'lot_number', 'quantity', 'expiration_date')
                 .order_by('ctm_name', 'lot_number'))

    # Get distinct Bulk CTM names for the dropdown
    unique_bulk_ctm_names = BulkCTM.objects.order_by('ctm_name').values_list('ctm_name', flat=True).distinct()

    # Serialize the data for Bulk CTMs
    bulk_ctms_json = mark_safe(json.dumps(list(bulk_ctms), cls=DjangoJSONEncoder))

    # Query for all depots and include address
    depots = list(Depot.objects.values('name', 'address'))

    # Serialize the depot data
    depots_json = mark_safe(json.dumps(depots, cls=DjangoJSONEncoder))

    # Create the context with all required data
    context = {
        'unique_individual_ctm_names': unique_individual_ctm_names,
        'unique_bulk_ctm_names': unique_bulk_ctm_names,
        'ctms_with_kits_json': ctms_with_kits_json,
        'bulk_ctms_json': bulk_ctms_json,  # Updated to include non-aggregated data
        'depots_json': depots_json,  # Updated to include address
        'depots': depots,
    }

    return render(request, 'supplier/depot_inventory_shipments.html', context)


@login_required
@permission_required('supplier.view_supplier_portal', login_url='error_page')
def create_inventory(request):
    bulk_form = BulkCTMForm(prefix='bulk')
    individual_form = IndividualCTMForm(prefix='individual')

    form = None  # Initialize the form variable here

    if request.method == "POST":
        ctm_type = request.POST.get('ctm_type')
        if ctm_type == 'bulk':
            form = BulkCTMForm(request.POST, prefix='bulk')
        elif ctm_type == 'individual':
            form = IndividualCTMForm(request.POST, prefix='individual')
        else:
            messages.error(request, 'Invalid CTM type.')

        if form is not None:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.ctm_type = ctm_type
                instance.save()
                messages.success(request, 'Form data saved successfully.')
                return redirect('supplier:create_inventory')
            else:
                messages.error(request, 'Form is not valid.')
                if ctm_type == 'bulk':
                    bulk_form = form  # reassign the form to retain the data
                else:
                    individual_form = form  # reassign the form to retain the data
        else:
            messages.error(request, 'Invalid form.')

    context = {
        'bulk_form': bulk_form,
        'individual_form': individual_form,
    }
    return render(request, 'supplier/create_inventory.html', context)


def is_kit_serial_number_unique(kit_serial_number):
    """ Check if the kit/serial number is unique across both inventories """
    in_temporary = TemporaryCTMInventory.objects.filter(kit_serial_number=kit_serial_number).exists()
    in_permanent = CTMInventory.objects.filter(kit_serial_number=kit_serial_number).exists()
    return not (in_temporary or in_permanent)


# Set up logging
logger = logging.getLogger(__name__)

@login_required
@permission_required('supplier.view_supplier_portal', login_url='error_page')
def process_ctm_entries(request):
    print("Processing CTM entries...")  # Print statement for initial entry
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            print("Data received:", data)  # Print the received data
            for item in data.get('individualCtm', []):
                print("Processing item:", item)  # Print each item being processed
                if not validate_ctm_entry(item) or not is_kit_serial_number_unique(item['kit_serial_number']):
                    print("Validation failed for item:", item)  # Print if validation fails
                    return JsonResponse({'error': 'Kit/Serial number already exists'}, status=400)

                page_session_id = item.get('page_session_id')
                print("Creating entry in TemporaryCTMInventory for session:", page_session_id)  # Print before creating entry
                TemporaryCTMInventory.objects.create(
                    page_session_id=page_session_id,
                    ctm_type='Individual',
                    ctm_name=sanitize_input(item['ctm_name']),
                    kit_serial_number=item['kit_serial_number'],
                    quantity=item['quantity'],
                    expiration_date=item['expiration_date'],
                    lot_number=item['lot_number']
                )
                print("Entry created successfully for session:", page_session_id)  # Print after entry creation
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("Exception occurred:", str(e))  # Print any exceptions
            return JsonResponse({'error': str(e)}, status=400)
    else:
        print("Invalid request method or header")  # Print if request method or header is not as expected
        return JsonResponse({'error': 'Invalid request'}, status=400)


# Validation Functions

def validate_ctm_entry(item):
    """ Validate each field of the CTM entry. """
    required_fields = ['kit_serial_number', 'expiration_date', 'ctm_name', 'lot_number']
    if not all(field in item for field in required_fields):
        return False
    return (validate_kit_serial_number_format(item['kit_serial_number']) and
            validate_expiration_date(item['expiration_date']) and
            validate_ctm_name_format(item['ctm_name']) and
            validate_lot_number_format(item['lot_number']))


def sanitize_input(input_string):
    """ Sanitize input to escape HTML characters """
    return html.escape(input_string)


def validate_kit_serial_number_format(kit_serial):
    """ Validate the kit/serial number format. """
    if not isinstance(kit_serial, str):
        return False
    return bool(re.match(r'^\d{5,10}$', kit_serial))


def validate_expiration_date(expiration_date_str):
    """ Validate the expiration date. """
    if not isinstance(expiration_date_str, str):
        return False
    try:
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
        return expiration_date > datetime.now().date()
    except ValueError:
        return False


def validate_ctm_name_format(ctm_name):
    """ Validate the CTM name format. """
    sanitized_name = sanitize_input(ctm_name)
    if not isinstance(sanitized_name, str):
        return False
    return len(sanitized_name) <= 100 and bool(re.match(r'^[a-zA-Z0-9\s]+$', sanitized_name))


def validate_lot_number_format(lot_number):
    """ Validate the lot number format. """
    if not isinstance(lot_number, str):
        return False
    return bool(re.match(r'^[A-Za-z0-9-]{3,20}$', lot_number))


def cleanup_expired_sessions():
    """
    Placeholder function for cleaning up expired sessions in TemporaryCTMInventory.
    TODO: Implement the actual cleanup logic.
    """
    # TODO: Implement logic to identify and delete expired session entries.
    # This could involve filtering TemporaryCTMInventory objects based on
    # criteria like 'created_at' timestamp and deleting them.

    pass  # Remove this line once the actual implementation is done.


@login_required
@permission_required('supplier.view_supplier_portal', login_url='error_page')
def supplier_inventory(request):
    individual_ctms = IndividualCTM.objects.all()
    bulk_ctms = BulkCTM.objects.all()

    context = {
        'individual_ctms': individual_ctms,
        'bulk_ctms': bulk_ctms,
    }
    return render(request, 'supplier/supplier_inventory.html', context)


@login_required
@permission_required('supplier.view_supplier_portal', login_url='error_page')
def returned_inventory(request):
    # You can add functionality here later
    return render(request, 'supplier/returned_inventory.html')
