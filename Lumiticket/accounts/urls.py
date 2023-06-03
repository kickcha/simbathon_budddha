from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
    path('loginpage/', loginpage, name="loginpage"),
]