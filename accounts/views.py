from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate

# Create your views here.
def signup(request):
    if request.method != "POST":
        return render(request,'accounts/signup.html')
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.get(username=username)
                return render(request,'accounts/signup.html',{'error':'Username has already been taken!!'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=username,password=password1)
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request,'accounts/signup.html',{'error':'Passwords must match!!'})


def login(request):
    if request.method != "POST":
        return render(request,'accounts/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'accounts/login.html',{'error':'Invalid login credentials.'})


def logout(request):
    if request.method != "POST":
        return render(request,'accounts/login.html')
    else:
        auth.logout(request)
        return redirect('home')