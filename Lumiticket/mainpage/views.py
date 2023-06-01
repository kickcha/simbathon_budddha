from django.shortcuts import render

def intropage(request):
    return render(request, 'mainpage/intropage.html')

def loadingpage(request):
    return render(request, 'mainpage/loadingpage.html')