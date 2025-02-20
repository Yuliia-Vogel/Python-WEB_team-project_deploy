from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'address', 'phone', 'email', 'birthday']
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 1}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "birthday": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        phone_regex = re.compile(r"^\+?\d{9,15}$")
        if not phone_regex.match(phone):
            raise forms.ValidationError(
                "Enter a valid phone number (9 to 15 digits, optionally starting with +)."
            )
        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError("Please enter a valid email address.")
        return email
