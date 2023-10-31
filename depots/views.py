from django.shortcuts import render

def depot_inventory(request):
    return render(request, 'depots/depot_inventory.html')

def depot_shipments(request):
    return render(request, 'depots/depot_shipments.html')

def returned_inventory(request):
    return render(request, 'depots/returned_inventory.html')
