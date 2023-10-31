from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm


def landing_page(request):
    form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})
