from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import views
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, UserVerifyForm
from .models import User, OneTimePass
import random
from datetime import datetime, timedelta
from django.contrib.auth import login, authenticate, logout
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
        now = datetime.now()
        expire_code = now + timedelta(minutes=2)
        form = self.form_class(request.POST)
        if form.is_valid():
            if now < expire_code:
                if form.cleaned_data['code'] == code_instance.code:
                    User.objects.create_user(user_session['email'], user_session['phone'], user_session['full_name'], user_session['password'])
                    user = authenticate(request, phone=user_session['phone'], password=user_session['password'])
                    login(request, user)
                    code_instance.delete()
                    messages.success(request, 'You registered succussfully!', 'success')
                    return redirect('home:home')
                else:
                    messages.error(request, 'Enterd code is wrong!', 'error')

                    return redirect('accounts:verify')
            else:
                messages.error(request, 'Your code is expierd!')
                code_instance.delete()
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
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfully.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            messages.error(request, 'Username or password is incorect!', 'error')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form' : form})