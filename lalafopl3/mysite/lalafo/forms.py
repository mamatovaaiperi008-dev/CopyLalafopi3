from django.views.generic import UpdateView

from .models import Product
from django import forms




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'phone_number', 'description','product_type','image']