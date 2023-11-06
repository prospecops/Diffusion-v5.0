import json

from django.contrib import messages  # Add this import at the beginning of your file
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Value as V, Q
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from django.shortcuts import render

from supplier.forms import BulkCTMForm, IndividualCTMForm
from supplier.models import BulkCTM
from .models import IndividualCTM


@login_required
@permission_required('supplier.view_supplier_portal', raise_exception=True)
def depot_inventory_shipments(request):
    # Your new query using aggregation
    ctms_with_kits = (IndividualCTM.objects
                      .values('ctm_name')
                      .annotate(kit_serial_numbers=ArrayAgg(Coalesce('kit_serial_number', V('N/A'))))
                      .filter(~Q(kit_serial_numbers=['N/A']))
                      .distinct()
                      .order_by('ctm_name'))

    # Converting to JSON
    ctms_with_kits_json = json.dumps(list(ctms_with_kits))

    # Print to console
    print(ctms_with_kits_json)  # This will print the JSON to the console where your server is running.

    # Render the template with the context containing the CTM names and related kits
    return render(request, 'supplier/depot_inventory_shipments.html', {
        'ctms_with_kits_json': ctms_with_kits_json
    })



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
