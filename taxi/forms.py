from django import forms
from .models import Driver, Car


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError("License must be exactly 8 characters")

        if not license_number[:3].isupper() \
                or not license_number[:3].isalpha():
            raise forms.ValidationError(
                "First 3 characters must be uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise forms.ValidationError("Last 5 characters must be digits")

        return license_number


class DriverCreateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "license_number",
        ]


class DriverUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "first_name",
            "last_name",
            "email",
            "license_number"
        ]


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
