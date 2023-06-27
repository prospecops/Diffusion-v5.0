from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    role = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.groups.add(self.cleaned_data['role'])  # add the user to the selected group
        user.save()
        return user
