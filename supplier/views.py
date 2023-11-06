from django.contrib import messages  # Add this import at the beginning of your file
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.db.models import F, Count
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from supplier.forms import BulkCTMForm, IndividualCTMForm
from supplier.models import BulkCTM
from .models import IndividualCTM


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
def depot_inventory_shipments(request):
    # Get unique ctm_names
    unique_ctm_names = IndividualCTM.objects.order_by('ctm_name').values_list('ctm_name', flat=True).distinct()

    # Render the template with the context containing the form and the unique CTM names
    return render(request, 'supplier/depot_inventory_shipments.html', {
        'unique_ctm_names': unique_ctm_names
    })



@login_required
@permission_required('supplier.view_supplier_portal', login_url='error_page')
def returned_inventory(request):
    # You can add functionality here later
    return render(request, 'supplier/returned_inventory.html')
