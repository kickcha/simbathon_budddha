from django.urls import path
from .views import * # accounts/views에서 모든 함수를 가져온다.

app_name = "mypage"
urlpatterns = [
    path('', mypage, name="mypage"),
]