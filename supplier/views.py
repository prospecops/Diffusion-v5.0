from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView
from supplier.models import BulkCTM, IndividualCTM
from supplier.forms import BulkCTMForm, IndividualCTMForm


@login_required
@permission_required('supplier.view_supplier_portal', login_url='error_page')
def supplier_portal(request):
    bulk_form = BulkCTMForm(prefix='bulk')
    individual_form = IndividualCTMForm(prefix='individual')
    context = {
        'bulk_form': bulk_form,
        'individual_form': individual_form,
    }
    return render(request, 'supplier/supplier_portal.html', context)



def add_ctm(request):
    if request.method == "POST":
        ctm_type = request.POST.get('ctm_type')
        if ctm_type == 'Bulk':
            form = BulkCTMForm(request.POST, prefix='bulk')
        else:
            form = IndividualCTMForm(request.POST, prefix='individual')

        if form.is_valid():
            form.save()
            return redirect('supplier:supplier_portal')
    else:
        return redirect('supplier:supplier_portal')



class CTMListView(ListView):
    template_name = "supplier/ctm_list.html"  # you'll create this template next
    context_object_name = "ctm_list"  # you can use this name in your template to access the list of CTMs

    def get_queryset(self):
        # we're including both bulk and individual CTMs in the list
        return BulkCTM.objects.all().union(IndividualCTM.objects.all())
