from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView
from supplier.models import BulkCTM, IndividualCTM
from supplier.forms import BulkCTMForm, IndividualCTMForm
from django.contrib import messages  # Add this import at the beginning of your file

@login_required
@permission_required('supplier.view_supplier_portal', login_url='error_page')
def create_inventory(request):
    bulk_form = BulkCTMForm(prefix='bulk')
    individual_form = IndividualCTMForm(prefix='individual')

    if request.method == "POST":
        ctm_type = request.POST.get('ctm_type')
        if ctm_type == 'bulk':
            form = BulkCTMForm(request.POST, prefix='bulk')
        elif ctm_type == 'individual':
            form = IndividualCTMForm(request.POST, prefix='individual')
        else:
            messages.error(request, 'Invalid CTM type.')
            form = None

        if form is not None:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.ctm_type = ctm_type
                instance.save()
                messages.success(request, 'Form data saved successfully.')
                return redirect('supplier:create_inventory')
            else:
                messages.error(request, 'Form is not valid.')
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
    # put code here to handle supplier inventory view
    return render(request, 'supplier/supplier_inventory.html')

@login_required
@permission_required('supplier.view_supplier_portal', login_url='error_page')
def depot_inventory_shipments(request):
    # put code here to handle depot inventory shipments view
    return render(request, 'supplier/depot_inventory_shipments.html')

class CTMListView(ListView):
    template_name = "supplier/ctm_list.html"  # you'll create this template next
    context_object_name = "ctm_list"  # you can use this name in your template to access the list of CTMs

    def get_queryset(self):
        # we're including both bulk and individual CTMs in the list
        return BulkCTM.objects.all().union(IndividualCTM.objects.all())
