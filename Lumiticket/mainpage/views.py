from django.shortcuts import render, redirect
from .models import Ticket
from django.utils import timezone
from qnapage import *

def detail(request, id):
    Ticket = get_object_or_404(Ticket, pk=id)
    return redirect(request, 'mainpage/ticketdetail.html', {ticket:ticket})

def intropage(request):
    return render(request, 'mainpage/intropage.html')

def loadingpage(request):
    return render(request, 'mainpage/loadingpage.html')

def mainpage(request): #로딩페이지 이후 페이지
    tickets = Ticket.objects.all()
    return render(request, 'mainpage/mainpage.html')

def create(request): #티켓 적는 함수
    new_ticket = Ticket()
    new_ticket.nickname = request.POST['nickname']
    new_ticket.pub_date = timezone.now()
    new_ticket.body = request.POST['body']

    new_ticket.save()
    return redirect('detail', new_ticket.id)

def new(request): #티켓 다 적은 뒤 로딩되는 페이지 정의
    return render(request, 'mainpage/ticketlistnew.html')

def qnalistnew(request):
    return render(request, 'qnapage/qnalistnew.html')
