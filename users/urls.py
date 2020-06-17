
from django.urls import path
import users.views as user_views
import django.contrib.auth.views as auth_views

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', user_views.logout_view, name='logout'),
]