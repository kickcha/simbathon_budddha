from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Comment
from django.utils import timezone
from qnapage import *
from accounts import *
from django.db.models import Count
from django.core.paginator import Paginator
# loading page관련 메서드
from django.template import loader
import time

def mainpage(request): #로딩페이지 이후 페이지
    #tickets = Ticket.objects.annotate(like_count=Count('like')).order_by('-like_count')[:2]
    return render(request, 'mainpage/mainpage.html')

def detail(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    if request.method == 'GET':
        comments = Comment.objects.filter(ticket=ticket)
        return render(request, 'mainpage/detail.html',{
            'ticket':ticket,
            'comments':comments,
            })
    elif request.method == "POST":
        new_comment = Comment()
        new_comment.ticket = ticket
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.pub_date = timezone.now()
        new_comment.save()

        return redirect('mainpage:detail', id)

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
    return render(request, 'mainpage/ticketlistnew.html')

def ticketlistpop(request):
    return render(reequest, 'mainpage/ticketlistpop.html')

def delete(request, id):
    if request.user.is_authenticated:
        delete_ticket = get_object_or_404(Ticket, id=id)
        delete_ticket.delete()
        return redirect('mainpage:ticketlistnew', id)
    return redirect('accounts:login')

def delete_comment(request, id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=id)
        ticket_id = comment.ticket.id
        comment.delete()
        return redirect('mainpage:detail', id=comment.ticket.id)
    return redirect('accounts:login')

def update_comment(request, id):
    if request.user.is_authenticated:
        update_comment = Comment.objects.get(id=id)
        if request.user == update_comment.writer:
            update_comment.pub_date = timezone.now()
            update_comment.content = request.POST['content']

            update_comment.save()
            return redirect('mainpage:detail', update_comment.id)
    return redirect('accounts:login')
