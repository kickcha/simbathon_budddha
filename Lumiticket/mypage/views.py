from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from mainpage.models import Ticket
from qnapage.models import *


def mypage(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login_required.html')
    else:
        user = request.user
        comments = QnaComment.objects.filter(writer=user)
        qnas = Qna.objects.filter(qnacomment__in=comments)
        context = {
            'user': user,
            'tickets': Ticket.objects.filter(writer=user),
            'comments': comments,
            'qnas': qnas,
        }
        return render(request, 'mypage/mypage.html', context)

def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'mainpage/detail.html', {'ticket':ticket})


def qnadetail(request, id):
    qna = get_object_or_404(Qna, pk=id)

    if request.method == 'GET':
        comments = QnaComment.objects.filter(qna=qna)
        return render(request, 'qnapage/qnadetail.html', {
            'qna': qna,
            'comments': comments
        })
    elif request.method == "POST":
        new_comment = QnaComment()
        new_comment.qna = qna
        new_comment.content = request.POST['content']
        new_comment.writer = request.user
        new_comment.pub_date = timezone.now()
        new_comment.save()

        # Refresh the qna object to reflect the new comment
        qna.refresh_from_db()

        return render(request, 'qnapage/qnadetail.html', {
            'qna': qna,
            'comments': QnaComment.objects.filter(qna=qna)
        })

    return render(request, 'qnapage/qnadetail.html', {'qna': qna})
