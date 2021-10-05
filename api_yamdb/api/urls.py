from django.urls import path

from . import views

urlpatterns = [
    path('v1/auth/signup/', views.signUp, name='signup'),
]