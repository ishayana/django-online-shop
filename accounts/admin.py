from django.contrib import admin
<<<<<<< HEAD
from django.contrib.auth.admin import UserAdmin
from accounts.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    ordering = ('email',)
    list_display = ('email', 'phone', 'full_name', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'phone', 'full_name', 'password', 'last_login')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Personal', {'fields': ('role', 'balance')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'full_name', 'password1', 'password2','balance', 'role','is_staff', 'is_active')}
        ),
    )
admin.site.register(User, CustomUserAdmin)
=======

# Register your models here.
>>>>>>> c314068622ef19aebf65029bd99c89c92da39472
