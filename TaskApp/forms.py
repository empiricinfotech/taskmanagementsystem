from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()


class DateInput(forms.DateInput):
    input_type = 'date'

class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True)
    password = forms.CharField(label="Password", required=True)

class passwordForm(forms.Form):
    newpassword = forms.CharField()
    confirmpassword = forms.CharField()
    
class editProfileForm(forms.ModelForm):
    password = None
    class Meta:
        model = User
        fields = ('username','email')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(email=self.instance.email).exists():
            raise forms.ValidationError("This email is already in use. Please choose a different one.")
        return email
  
class createTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_title','assign_To','startDate','endDate','status','progress','priority','dependency','description')
        widgets = {
            'startDate': DateInput,
            'endDate': DateInput,
            'dependency': forms.CheckboxSelectMultiple(),
        }   
    
        
        