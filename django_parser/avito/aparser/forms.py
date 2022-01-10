from django import forms

from .models import Product
from .models import Profile
from .models import Rent


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title',
            'price',
            'address',
            'url',
            'published_date',
        )
        widgets = {
            'title': forms.TextInput,
        }


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = (
            'title',
            'price',
            'srok',
            'address',
            'url',
            'published_date',
        )
        widgets = {
            'title': forms.TextInput,
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'external_id',
            'name',
        )
        widgets = {
            'name': forms.TextInput,
        }
