from  django import forms
from  django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth.models import User
from django.views.generic import UpdateView


class SignUpForm(UserCreationForm):
  

    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
  
   
    
   
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
        


class UserUpdateView(UpdateView):
    phone = forms.CharField(max_length=255, required=True, widget=forms.NumberInput())


    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'password1', 'password2','phone'}
        




