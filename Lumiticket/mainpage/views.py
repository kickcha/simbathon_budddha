from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket
from django.utils import timezone
from qnapage import *
from accounts import *
# loading page관련 메서드
from django.template import loader
import time

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

def likes(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user in ticket.like.all():
        ticket.like.remove(request.user)
        ticket.like_count -= 1
        ticket.save()
    else:
        ticket.like.add(request.user)
        ticket.like_count += 1
        ticket.save()
    return redirect('mainpage:deatil', ticket.id)

def ticketlistnew(request):
    return redirect('mainpage:ticketlistnew')

def ticketlistpop(request):
    return redirect('mainpage:ticketlistpop')

def delete(request, id):
    delete_ticket = Ticket.objects.get(id=id)
    delete_blog.delete()
    return redirect('mainpage:ticketlistnew')