from django.shortcuts import render


# def home_request(request):
#     return render(request=request, template_name='account/../core/templates/home.html')


def landing_page(request):
    return render(request, 'account/landing.html')

