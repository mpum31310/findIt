from django import forms
from .models import Child


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ('name', 'surname', 'grade', 'school')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

