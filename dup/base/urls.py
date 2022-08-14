from os import lseek
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name= "home"), 
    path('login/', views.loginPage, name="login"),
    path('profile/<int:pk>/', views.userProfile, name="user-profile"),

    path('room/<str:pk>/', views.room, name="room"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('create-room/', views.CreateRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateroom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deletemessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    # path('change-password/', auth_views.PasswordResetView.as_view(), name="reset-password"),
    # path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name="reset-password-sent"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="reset-password-confirm"),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="reset-password-complete"),
]