from django.shortcuts import render
from .models import DepotInventory
from django.contrib.auth.decorators import login_required, permission_required


# depots/views.py

@login_required
@permission_required('depots.view_depot_portal', login_url='error_page')
def depot_inventory(request):
    # Assuming user's profile or another mechanism associates a user with a specific depot
    user_depot = request.user.depot
    depot_inventory = DepotInventory.objects.filter(depot=user_depot)

    context = {
        'depot_inventory': depot_inventory,
    }
    return render(request, 'depots/depot_inventory.html', context)


@permission_required('depots.view_depot_portal', raise_exception=True)
def depot_shipments(request):
    return render(request, 'depots/depot_shipments.html')


@permission_required('depots.view_depot_portal', raise_exception=True)
def returned_inventory(request):
    return render(request, 'depots/returned_inventory.html')
