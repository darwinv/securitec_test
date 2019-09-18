from django import forms


class ContactForm(forms.Form):
    """Formulario."""
    CHOICES = (('cd', 'CD'), ('nc', 'NC'),)
    tipo_contacto = forms.CharField(widget=forms.Select(attrs={
        'class': 'form-control', 'placeholder': 'tipo'
        }, choices=CHOICES), required=True, label='Tipo')
