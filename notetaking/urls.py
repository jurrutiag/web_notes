"""Map the requests to the corresponding response inside the app."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_note, name='notetaking-home'),
    path('login/', views.login, name='notetaking-login'),
]
