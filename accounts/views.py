from django.shortcuts import render
from django.contrib.auth import views
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm

class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        pass

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        pass