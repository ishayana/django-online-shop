from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

# You can use the forms.form but you must write confirmation passwords and override save
class CustomUserCreationForm(UserCreationForm):
    # password = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password1 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'phone', 'full_name', 'role')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        fields = ('email', 'phone', 'full_name', 'role', 'balance', 'is_active', 'is_staff')


class UserRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = False
            field.widget.attrs['class'] = 'fields'
    full_name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder' : 'Fullname'}))
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'placeholder' : 'Phone number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder' : 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))

    def clean_email(self): 
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            raise ValidationError('This email address is already in use.')
        except User.DoesNotExist:
            return email
        
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        try:
            User.objects.get(phone=phone)
            raise ValidationError('This phone-number is already is use.')
        except User.DoesNotExist:
            print('except operate')
            return phone


class UserVerifyForm(forms.Form):
    code = forms.IntegerField(label=False, widget=forms.TextInput(attrs={'placeholder' : 'Enter code', 'class' : 'fields'}))

class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'fields'
            field.label = False

    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'placeholder' : 'Phone number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))