from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    item_qr_data = forms.CharField(max_length=500, required=True, widget=forms.HiddenInput())

    class Meta:
        model = Message
        fields = ('sender_name', 'sender_email', 'sender_phone', 'message', 'item_qr_data')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sender_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['sender_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['sender_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['sender_email'].required = False
        self.fields['sender_phone'].required = False

