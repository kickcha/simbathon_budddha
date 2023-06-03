from django.shortcuts import render

# Create your views here.
def loginpage(request):
    return render(request, 'accounts/loginpage.html')

# acccounts/login -> 구글
# login -> 원하는 페이지로 안갈수도 있다. 