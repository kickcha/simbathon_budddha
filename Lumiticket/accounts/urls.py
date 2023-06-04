from django.urls import path
from .views import * # accounts/views에서 모든 함수를 가져온다.

app_name = "accounts"
urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name="signup"),
]