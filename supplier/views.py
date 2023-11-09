import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.shortcuts import render, redirect

from .forms import BulkCTMForm, IndividualCTMForm
from .models import IndividualCTM, BulkCTM
from django.utils.safestring import mark_safe
from django.core.serializers.json import DjangoJSONEncoder


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
    unique_individual_ctm_names = IndividualCTM.objects.order_by('ctm_name').values_list('ctm_name', flat=True).distinct()

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


    # Create the context with all required data
    context = {
        'unique_individual_ctm_names': unique_individual_ctm_names,
        'unique_bulk_ctm_names': unique_bulk_ctm_names,
        'ctms_with_kits_json': ctms_with_kits_json,
        'bulk_ctms_json': bulk_ctms_json,  # Updated to include non-aggregated data
        # Add any other context variables you might need
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
