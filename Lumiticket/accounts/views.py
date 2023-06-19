from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile # 모델 사용

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authentication(request, username = username, password = password)
        if user is not None:
            auth.login(request,user)
            return redirect('mainpage:mainpage')
        else:
            return render(request, 'accounts/login.html') # '정보 없음, 회원가입 물어보는 페이지' 가기로 바꾸기
        
    elif request.method == 'GET':
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('mainpage:mainpage')

def signup(request):
    if request.method == 'POST':
        # 변수 받아오기
        username = request.POST['username']
        nickname = request.POST['nickname']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if not username or not password:
            error_username = '아이디와 비밀번호를 입력해주세요.'
            return render(request, 'accounts/signup.html', {'error_username': error_username})
        if not nickname:
            error_nickname = '닉네임을 입력해주세요.'
            return render(request, 'accounts/signup.html', {'error_nickname': error_nickname})
        elif Profile.objects.filter(nickname=nickname).exists():
            error_nickname = '이미 사용중인 닉네임입니다.'
            return render(request, 'accounts/signup.html', {'error_nickname': error_nickname})
        if password != confirm:
            error_password = '비밀번호와 비밀번호 확인이 일치하지 않습니다.'
            return render(request, 'accounts/signup.html', {'error_password': error_password})
        else:
            user = User.objects.create_user(username=username, password=password)

            profile = Profile(user=user, nickname=nickname)
            profile.save()

            auth.login(request,user)
            return redirect('mainpage:mainpage')
        
    return render(request, 'accounts/signup.html') # 