from django.urls import path
from . import views

urlpatterns = {
    path('', views.Home, name='home'),
    path('login/', views.loginPage, name="login"), 
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerUser, name="register"),


}