from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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