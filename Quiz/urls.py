from django.urls import path

from . import views

app_name= "Quiz"
urlpatterns = [
    path('', views.signupPage , name='signup'),
]


