from django.urls import path

from . import views

app_name= "Quiz"
urlpatterns = [
    path('', views.signupPage , name='signup'),
    path('login/', views.loginPage , name='login'),
    path('home/', views.HomePage , name='home'),
    path('logout/', views.logoutpage , name='logout'),
    path('creatprofile/<int:id>', views.creatprofilePage , name='creatprofile'),
    path('profile/<int:id>', views.profilePage , name='profile'),
    path('updateprofile/<int:id>', views.updateprofilePage , name='updateprofile'),
    path('api/get-quiz/', views.get_quiz, name='get_quiz'),
]



