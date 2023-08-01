from django.shortcuts import render

# Create your views here.

def HomePage(request):
    pass

def loginPage(request):
    pass

def signupPage(request):
    return render(request,'Quiz/signup.html')
