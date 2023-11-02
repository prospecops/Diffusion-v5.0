from django.shortcuts import render
from django.contrib.auth.decorators import permission_required


@permission_required('depots.view_depot_portal', raise_exception=True)
def depot_inventory(request):
    return render(request, 'depots/depot_inventory.html')


@permission_required('depots.view_depot_portal', raise_exception=True)
def depot_shipments(request):
    return render(request, 'depots/depot_shipments.html')


@permission_required('depots.view_depot_portal', raise_exception=True)
def returned_inventory(request):
    return render(request, 'depots/returned_inventory.html')
