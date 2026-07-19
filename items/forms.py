from django import forms
from django.core.exceptions import ValidationError
from children.models import Child
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'child', 'item_image')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'item_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'child': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['child'].required = False
        self.fields['child'].empty_label = '— Select a child —'
        if user:
            self.fields['child'].queryset = Child.objects.filter(parent=user)
        else:
            self.fields['child'].queryset = Child.objects.none()

    def clean_child(self):
        child = self.cleaned_data.get('child')
        if child and self.user and child.parent_id != self.user.id:
            raise ValidationError('Please select one of your children.')
        return child
