from django.urls import path
from .views import * # accounts/views에서 모든 함수를 가져온다.

app_name = "accounts"
urlpatterns = [
    path('real_login/', real_login, name="real_login"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name="signup"),
]