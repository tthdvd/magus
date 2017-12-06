from django import forms
from finder.models import Resources
from django.contrib.auth.models import User

class ResourcesForm(forms.Form):
    name = forms.CharField()
    name.widget.attrs['class'] = 'form-control'

    date_in = forms.DateField()
    date_in.widget.input_type = 'date'
    date_in.widget.attrs['class'] = 'form-control'

    date_out = forms.DateField(required=False)
    date_out.widget.input_type = 'date'
    date_out.widget.attrs['class'] = 'form-control'

    def saveData(self):
        resources = Resources()
        resources.name = self.cleaned_data.get('name')
        resources.date_in = self.cleaned_data.get('date_in')
        resources.date_out = self.cleaned_data.get('date_out')
        resources.save()
        return resources


class CreateUserForm(forms.Form):
    username = forms.CharField()
    username.widget.attrs['class'] = 'form-control'

    email = forms.EmailField()
    email.widget.attrs['class'] = 'form-control'

    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password1.widget.attrs['class'] = 'form-control'

    password2 = forms.CharField(widget=forms.PasswordInput(), label="Password Confirm")
    password2.widget.attrs['class'] = 'form-control'

    first_name = forms.CharField()
    first_name.widget.attrs['class'] = 'form-control'

    last_name = forms.CharField()
    last_name.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']

        raise forms.ValidationError("this user exist already")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords dont match each other")

        return self.cleaned_data

    def saveData(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                            password=self.cleaned_data['password1'],
                                            email=self.cleaned_data['email'],
                                            )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()