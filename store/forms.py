from django import forms
from django.forms import ModelForm
from .models import ContactMessage

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    cat = forms.IntegerField()


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage  

        fields = ['name','email','subject','message']    
        widget = {
            'subject':forms.TextInput(attrs={'class': 'form-control','placeholder':'sub'}),
            'email':forms.EmailInput(attrs={'class': 'form-control','placeholder':'sub'}),
            'subject':forms.TextInput(attrs={'class': 'form-control','placeholder':'sub'}),
            'message':forms.TextInput(attrs={'class': 'form-control','placeholder':'sub'})


        }    

        
   
