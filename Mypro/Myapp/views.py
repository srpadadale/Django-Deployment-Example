from django.shortcuts import render
from Myapp.forms import UserInfoForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
def index(request):
    return render(request,'Myapp/index.html')

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserInfoForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserInfoForm()
        profile_form = UserProfileInfoForm()

    return render(request,'Myapp/register.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Your account is not active!")

        else:
            return HttpResponse("You need to signup!")

    else:
        return render(request,'Myapp/login.html')
