from django.shortcuts import render


def ctm_tracking_home(request):
    return render(request, 'ctm_tracking/ctm_tracking_home.html')


def drug_inventory(request):
    return render(request, 'ctm_tracking/drug_inventory.html')


def drug_shipments(request):
    return render(request, 'ctm_tracking/drug_shipments.html')


def drug_request(request):
    return render(request, 'ctm_tracking/drug_request.html')


def accountability(request):
    return render(request, 'ctm_tracking/accountability.html')


def final_disposition(request):
    return render(request, 'ctm_tracking/final_disposition.html')
