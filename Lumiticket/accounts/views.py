from django.shortcuts import render, redirect

# Create your views here.
def login(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        return render(request, 'accounts/login.html')

# acccounts/login -> 구글
# login -> 원하는 페이지로 안갈수도 있다. 