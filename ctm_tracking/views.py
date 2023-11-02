from django.shortcuts import render
from django.contrib.auth.decorators import permission_required


@permission_required('ctm_tracking.view_ctm_tracking_portal', raise_exception=True)
def ctm_tracking_home(request):
    return render(request, 'ctm_tracking/ctm_tracking_home.html')


@permission_required('ctm_tracking.view_ctm_tracking_portal', raise_exception=True)
def drug_inventory(request):
    return render(request, 'ctm_tracking/drug_inventory.html')


@permission_required('ctm_tracking.view_ctm_tracking_portal', raise_exception=True)
def drug_shipments(request):
    return render(request, 'ctm_tracking/drug_shipments.html')


@permission_required('ctm_tracking.view_ctm_tracking_portal', raise_exception=True)
def drug_request(request):
    return render(request, 'ctm_tracking/drug_request.html')


@permission_required('ctm_tracking.view_ctm_tracking_portal', raise_exception=True)
def accountability(request):
    return render(request, 'ctm_tracking/accountability.html')


@permission_required('ctm_tracking.view_ctm_tracking_portal', raise_exception=True)
def final_disposition(request):
    return render(request, 'ctm_tracking/final_disposition.html')
