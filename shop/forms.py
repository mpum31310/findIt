from django import forms
from django.utils.text import slugify

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name', 'category', 'description', 'price', 'pack_size',
            'image', 'is_active', 'sort_order',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'sort_order': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-control')
        self.fields['image'].widget.attrs.setdefault('class', 'form-control')

    def save(self, commit=True):
        product = super().save(commit=False)
        if not product.slug:
            base_slug = slugify(product.name) or 'product'
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            product.slug = slug
        if commit:
            product.save()
        return product


class CheckoutForm(forms.Form):
    shipping_name = forms.CharField(max_length=200, label='Full name')
    shipping_phone = forms.CharField(max_length=20, label='Cell number')
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Delivery address',
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        label='Order notes (optional)',
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
        if user:
            full_name = f'{user.first_name} {user.last_name}'.strip()
            if full_name:
                self.fields['shipping_name'].initial = full_name
            if getattr(user, 'cell_number', None):
                self.fields['shipping_phone'].initial = user.cell_number
