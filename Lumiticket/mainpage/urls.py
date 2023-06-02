from django.urls import path
from .views import *

app_name = "mainpage"
urlpatterns = [
    path('', intropage, name="introage"),
    path('loadingpage/', loadingpage, name="loadingpage"),
    path('new/', new, name="new"),
    path('create/', create, name="create"),
]