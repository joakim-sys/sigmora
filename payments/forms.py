from django import forms


class OrderForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    preferred_platforms = forms.CharField(max_length=255)
    customization_notes = forms.CharField(widget=forms.Textarea, required=False)
