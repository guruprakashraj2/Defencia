from django import forms
from django.contrib.auth.models import User
import re 
from django.contrib.auth import authenticate
from django import forms
from .models import Contact

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', max_length=100, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', max_length=100, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Check length
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        
        # Check for lowercase
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")

        # Check for special character
        if not re.search(r'[^A-Za-z0-9]', password):
            raise forms.ValidationError("Password must contain at least one special character.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            self.user = user  # Save user for use in view

        return cleaned_data
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered.")
        return email

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password")
        password2 = cleaned_data.get("confirm_password")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
