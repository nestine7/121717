from django import forms
from .models import Code
class CodeForm(forms.ModelForm):
    number=forms.CharField(label='Code',help_text='Enter SMS verification code')
    class Meta:
        model=Code
        fields=('number',)
class RegistrationForm(forms.ModelForm):
    username=forms.CharField(label='Username',help_text='Enter a unique username')
    password=forms.CharField(label='Password',help_text='6 characters min')
    