from django.urls import path

from . import views

app_name= "Quiz"
urlpatterns = [
    path('', views.signupPage , name='signup'),
    path('login/', views.loginPage , name='login'),
    path('home/', views.HomePage , name='home'),
    path('logout/', views.logoutpage , name='logout'),
]



