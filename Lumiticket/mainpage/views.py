from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Comment
from django.utils import timezone
from qnapage import *
from accounts import *
from django.db.models import Count, F
from django.core.paginator import Paginator
# loading page관련 메서드
from django.template import loader
import time

def mainpage(request): 
    tickets = Ticket.objects.order_by('-like_count')[:2]
    return render(request, 'mainpage/mainpage.html', {'tickets': tickets})

def detail(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    return render(request, 'mainpage/detail.html',{'ticket':ticket})

def intropage(request):
    return render(request, 'mainpage/intropage.html')

def loadingpage(request):
    return render(request, 'mainpage/loadingpage.html')

def new(request):
    return render(request, 'mainpage/new.html')

def create(request): #티켓 적는 함수
    if request.user.is_authenticated:
        new_ticket = Ticket()
        #profile = Profile.objects.get(user=request.user) #profile 가져오는 거
        
        new_ticket.writer = request.user #profile.nickname #request.user.profile.nickname
        new_ticket.pub_date = timezone.now()
        new_ticket.body = request.POST['body']
        new_ticket.save()
        
        return redirect('mainpage:detail', new_ticket.id)

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
    return redirect('mainpage:detail', ticket.id)

def ticketlistnew(request): 
    ticket_list = Ticket.objects.order_by('-pub_date')
    paginator = Paginator(ticket_list, 4)
    page = request.GET.get('page')
    tickets = paginator.get_page(page)

    return render(request, 'mainpage/ticketlistnew.html', {'tickets':tickets})

def ticketlistpop(request):
    ticket_list = Ticket.objects.order_by('-like_count')
    paginator = Paginator(ticket_list, 4)
    page = request.GET.get('page')
    tickets = paginator.get_page(page)

    return render(request, 'mainpage/ticketlistpop.html', {'tickets':tickets})

def delete(request, id):
    if request.user.is_authenticated:
        delete_ticket = get_object_or_404(Ticket, id=id)
        delete_ticket.delete()
        return redirect('mainpage:mainpage')
    return redirect('accounts:login')
