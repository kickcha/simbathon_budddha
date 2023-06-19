from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket
from django.utils import timezone
from qnapage import *
from accounts import *

def detail(request, id):
    ticket = get_object_or_404(Ticket, pk=username)
    return render(request, 'mainpage/detail.html', {'ticket':ticket})

def intropage(request):
    return render(request, 'mainpage/intropage.html')

def loadingpage(request):
    return render(request, 'mainpage/loadingpage.html')

def mainpage(request): #로딩페이지 이후 페이지
    tickets = Ticket.objects.all()
    return render(request, 'mainpage/mainpage.html', {'tickets':tickets})

def new(request):
    return render(request, 'mainpage/new.html')

def create(request): #티켓 적는 함수
    if request.user.is_authenticated:
        new_ticket = Ticket()
        new_ticket.writer = request.user.profile.nickname
        new_ticket.pub_date = timezone.now()
        new_ticket.body = request.POST['body']
        new_ticket.save()
        
        return redirect('mainpage:detail', username=new_ticket.username)

    else:
        return redirect('accounts:login')

def ticketlistnew(request): #티켓 다 적은 뒤 로딩되는 페이지 정의
    return render(request, 'mainpage/ticketlistnew.html')

def qnalistnew(request):
    return render(request, 'qnapage/qnalistnew.html')
