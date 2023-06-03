from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')

# acccounts/login -> 구글
# login -> 원하는 페이지로 안갈수도 있다. 