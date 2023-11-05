from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView

from depots.models import DepotInventory
from supplier.models import BulkCTM, IndividualCTM
from supplier.forms import BulkCTMForm, IndividualCTMForm, AssignInventoryForm
from django.contrib import messages  # Add this import at the beginning of your file


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
    if request.method == "POST":
        form = AssignInventoryForm(request.POST)
        if form.is_valid():
            selected_depot = form.cleaned_data.get("depot")
            selected_bulk_ctms = form.cleaned_data.get("bulk_ctms")
            selected_individual_ctms = form.cleaned_data.get("individual_ctms")

            # Assigning selected BulkCTMs and IndividualCTMs to the depot
            for bulk_ctm in selected_bulk_ctms:
                bulk_ctm.depot = selected_depot
                bulk_ctm.save()
                # Create or update the DepotInventory for bulk_ctm
                DepotInventory.objects.update_or_create(
                    depot=selected_depot,
                    bulk_ctm=bulk_ctm,
                    defaults={'quantity_received': bulk_ctm.quantity}
                )

            for individual_ctm in selected_individual_ctms:
                individual_ctm.depot = selected_depot
                individual_ctm.save()
                # Create or update the DepotInventory for individual_ctm
                DepotInventory.objects.update_or_create(
                    depot=selected_depot,
                    individual_ctm=individual_ctm,
                    defaults={'quantity_received': individual_ctm.quantity}
                )

            messages.success(request, 'Inventory assigned to depot successfully.')
            return redirect('supplier:depot_inventory_shipments')  # Redirect to a success page or the same page to show success message

    form = AssignInventoryForm()
    return render(request, 'supplier/depot_inventory_shipments.html', {"form": form})



@login_required
@permission_required('supplier.view_supplier_portal', login_url='error_page')
def returned_inventory(request):
    # You can add functionality here later
    return render(request, 'supplier/returned_inventory.html')


class CTMListView(ListView):
    template_name = "supplier/ctm_list.html"  # you'll create this template next
    context_object_name = "ctm_list"  # you can use this name in your template to access the list of CTMs

    def get_queryset(self):
        # we're including both bulk and individual CTMs in the list
        return BulkCTM.objects.all().union(IndividualCTM.objects.all())

@login_required
@permission_required('supplier.view_supplier_portal', login_url='error_page')
def individual_ctm_form_view(request):
    form = IndividualCTMForm()  # Instantiate your form
    # Logic to handle form submission if method is POST
    return render(request, 'individual_ctm_form.html', {'form': form})
