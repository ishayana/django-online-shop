from django.shortcuts import render, redirect
from django.contrib.auth import views
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, UserVerifyForm
from .models import User, OneTimePass
import random
from .utils import send_sms
from django.contrib import messages

class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            cd = form.cleaned_data
            send_sms(cd['phone'], random_code)
            OneTimePass.objects.create(phone=cd['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone' : cd['phone'],
                'full_name' : cd['full_name'],
                'email' : cd['email'],
                'password' : cd['password']
            }
            messages.success(request, 'Check your phone, We sent you a code', 'info')
            return redirect('accounts:verify')
        return render(request, self.template_name, {'form' : form})


class UserVerifyView(View):
    form_class = UserVerifyForm
    template_name = 'accounts/verify.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form' : form})
    
    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OneTimePass.objects.get(phone=user_session['phone'])
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] == code_instance.code:
                User.objects.create_user(user_session['email'], user_session['phone'], user_session['full_name'], user_session['password'])
                code_instance.delete()
                messages.success(request, 'You registered succussfully!', 'success')
                print('code success!')
                return redirect('home:home')
            else:
                messages.error(request, 'Enterd code is wrong!', 'error')
                print('code wrong!')
                return redirect('accounts:verify')
        else:
            return render(request, self.template_name, {'form' : form})



class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        pass