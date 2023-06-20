from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def mypage(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login_required.html')
    else:
        user = request.user
        context = {
            'user': user,
        }   
        return render(request, 'mypage/mypage.html', context)
# Create your views here.
