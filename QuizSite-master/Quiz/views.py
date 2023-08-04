from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .models import Question, Choice

from django.views import generic

import random


# Create your views here.

def HomePage(request):
    question = random.choice(list(Question.objects.all()))
    context = {
        'question': question,
    }
    
    return render(request, 'Quiz/home.html', context)

def loginPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=uname, password=pass1)

        if user is not None:
            login(request,user)
            return redirect("Quiz:home")
        else:
            return HttpResponse("username or password is incorrect")
    return render(request,'Quiz/login.html')

def signupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse ("your passwoerd and confirm password is not same!!")
        else:

           my_user=User.objects.create_user(uname,email,pass1)
           my_user.save()
           return redirect("Quiz:login")
    

    return render(request,'Quiz/signup.html')

def logoutpage(request):
    logout(request)
    return redirect('Quiz:login')