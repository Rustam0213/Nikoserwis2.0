import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Applications
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.forms.widgets import SplitDateTimeWidget
from django.core.exceptions import ValidationError
from datetime import date

class UserCreationForm(UserCreationForm):

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
        required=True,
    )

    phone = forms.CharField(
        label=_("Phone"),
        max_length=15,
        widget=forms.TextInput(attrs={"autocomplete": "tel", "pattern": "[0-9]*"}),
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].required = True

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Taki użytkownik już istnieje.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Użytkownik z tym adresem e-mail już istnieje.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie są zgodne.")
        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return phone

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone','is_active', 'is_staff', 'is_superuser',"groups"]

day = date.today()

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ['vin_code', 'reg_num', 'mark', 'model', 'year', 'displacement', 'hp', 'details', 'desired_appointment_date']
    
    year = forms.IntegerField(required=True)
    displacement = forms.DecimalField(required=True, max_digits=5, decimal_places=2)
    hp = forms.IntegerField(required=True)
    desired_appointment_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'id': 'id_desired_date', 'value' : day, 'min':day}),
        label='Data'
    )

    def clean_year(self):
        year = self.cleaned_data['year']
        if not 1800 <= year <= 2100:
            raise forms.ValidationError("Wprowadź poprawny rok.")
        return year


class VerificationCodeForm(forms.Form):
    verification_code = forms.IntegerField()