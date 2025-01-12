from django.urls import path
from . import views as users_views

urlpatterns = [
    path('login/', users_views.LoginView, name='login'),
    path('register/', users_views.RegisterView, name='register'),
    path('logout/', users_views.LogoutView, name='logout'),
]
