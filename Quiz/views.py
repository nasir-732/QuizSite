from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.models import User 
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
import random


# Create your views here.

def HomePage(request):
    context = {'categories' : Category.objects.all()}

    # if request.GET.get('category'):
    #     return redirect(f"Quiz/quiz/?category={request.GET.get('category')}")
    return render (request , 'Quiz/home.html', context)

def Quiz(request):
    context = {'category'  : request.GET.get('category')}
    return render(request, "Quiz/quiz.html" , context)
    # user = request.user
    # print(user.id)
    # return render(request,'Quiz/home.html')

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
           print("my,user",my_user)
           return redirect("Quiz:login")
    

    return render(request,'Quiz/signup.html')

def logoutpage(request):
    logout(request)
    return redirect('Quiz:login')

def creatprofilePage(request , id):
    user = request.user
    if request.method =='POST':
        bio=request.POST.get('bio')
        image=request.FILES.get('image') if 'image' in request.FILES else None
        print(image)
        user_profile = Userprofile.objects.create(
            user=request.user,
            bio=bio,
            image=image
        ) 
        user_profile.save()
        return redirect('Quiz:profile',id)
        # return redirect("Quiz:profile")

    return render(request,'Quiz/creatprofile.html')

def profilePage(request, id):
    # user = request.user
    user = get_object_or_404(User, pk = id)
    # print(user)
    # return HttpResponse("profile")
    user_profie=Userprofile.objects.filter(user=user.id)
    # print(user_profie)
    
    return render(request,'Quiz/profile.html',{'profile':user_profie})
# 

def updateprofilePage(request, id):
    user = get_object_or_404(User, pk=id)
    user_profile, created = Userprofile.objects.get_or_create(user=user)

    context = {
        'user': user,
        'user_profile': user_profile,
    }

    if request.method == 'POST':
        new_bio = request.POST.get('bio')
        new_image=request.FILES.get('image') if 'image' in request.FILES else None
        user_profile.bio = new_bio
        user_profile.image = new_image
        
        user_profile.save()

        return redirect('Quiz:profile', id=id)

    return render(request, 'Quiz/updateprofile.html', context)

def get_quiz(request):
    try:
        question_objs =Question.objects.all()

        if request.POST.get('quiz_category'):
            question_objs= question_objs.filter(category__category_name__icontains=request.POST.get('quiz_category'))
        question_objs= list(question_objs)    
        data=[]
        random.shuffle((question_objs))

        print(question_objs)
        for question_obj in question_objs:
            data.append({
                "uid":question_obj.uid,
                "Category":question_obj.category.category_name,
                "question":question_obj.question,
                "marks":question_obj.marks,
                "answers":question_obj.get_answers()
            })
        payload={'status' : True , 'questions' : data, 'questions_list': ','.join([str(i.pk) for i in question_objs])}

        
        return render(request, "Quiz/quiz.html" , payload)

        # return JsonResponse(payload)
      


    except Exception as e:
        print(e) 
    return HttpResponse("something went wrong")  

def result(request):
    given_questions = request.POST.getlist('questions_list')
    result = 0

    for q in given_questions:
        user_selected_choice_for_q = request.POST.get(q)
        correct_answer = Answer.objects.get(question__uid=q, is_correct=True)

        if user_selected_choice_for_q == correct_answer.answer:
            result += 1

    print(result)
    
    return render(request, 'Quiz/result.html', {'results': result})


def quiz_view(request):
    if request.method == 'POST':
        # Handle quiz submission here
        # ...
        return render(request, "Quiz/quiz.html")