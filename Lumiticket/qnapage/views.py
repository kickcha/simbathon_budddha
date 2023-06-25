from django.shortcuts import render, redirect, get_object_or_404
from .models import Qna, QnaComment, QnaReply
from django.utils import timezone
from django.db.models import Max
from django.db.models import Count


# Create your views here.
def create(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login_required.html')
    else:
        new_qna = Qna()
        new_qna.title = request.POST['title']
        new_qna.writer = request.user
        new_qna.pub_date = timezone.now()
        new_qna.body = request.POST['body']
        new_qna.save()
        return redirect('qnapage:qnalistrecent')

def new(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login_required.html')
    else:
        return render(request, 'qnapage/newqna.html')

def qnalistrecent(request):
    qnas = Qna.objects.annotate(comment_count=Count('qnacomment'), reply_count=Count('qnacomment__qnareply')).order_by('-pub_date')
    return render(request, 'qnapage/qnalistrecent.html', {'qnas':qnas})

def qnalistpop(request):
    qnas = Qna.objects.annotate(
        comment_count=Count('qnacomment'), 
        reply_count=Count('qnacomment__qnareply'),
        latest_comment_date=Max('qnacomment__pub_date')
        ).order_by('-latest_comment_date')
    return render(request, 'qnapage/qnalistpop.html', {'qnas': qnas})

def qnadetail(request, id):
    qna = get_object_or_404(Qna, pk = id)
    if request.method == 'GET':
        comments = QnaComment.objects.filter(qna = qna)
        total_count = comments.count() + QnaReply.objects.filter(comment__in=comments).count()
        return render(request, 'qnapage/qnadetail.html',{
            'qna':qna,
            'comments':comments,
            'total_count':total_count,
            })
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, 'accounts/login_required.html')
        else:
            new_comment = QnaComment()
            # foreignkey > blog 객체 직접 넣어주기
            new_comment.qna = qna
            # foreignkey > request.user 객체 직접 넣어주기
            new_comment.content = request.POST['content']
            new_comment.writer = request.user
            new_comment.pub_date = timezone.now()
            new_comment.save()
            return redirect('qnapage:qnadetail', id)
    return render(request, 'qnapage/qnadetail.html', {'qna':qna})

def comment_likes(request, comment_id):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login_required.html')
    else:
        qnacomment = get_object_or_404(QnaComment, id=comment_id)
        if request.user in qnacomment.comment_like.all():
            qnacomment.comment_like.remove(request.user)
            qnacomment.comment_like_count -= 1
            qnacomment.save()
        else:
            qnacomment.comment_like.add(request.user)
            qnacomment.comment_like_count += 1
            qnacomment.save()
        return redirect('qnapage:qnadetail', qnacomment.qna.id)

def comment_delete(request, comment_id):
    comment = get_object_or_404(QnaComment, id=comment_id)
    qna_id = comment.qna.id
    if request.method == 'POST' and request.user == comment.writer:
        comment.delete()
    return redirect('qnapage:qnadetail', qna_id)

def reply_create(request, comment_id):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login_required.html')
    else:
        comment = get_object_or_404(QnaComment, id=comment_id)
        if request.method == 'POST':
            content = request.POST['content']
            writer = request.user
            pub_date = timezone.now()
            QnaReply.objects.create(content=content, writer=writer, pub_date=pub_date, comment=comment)
        return redirect('qnapage:qnadetail', comment.qna.id)

def reply_delete(request, reply_id):
    reply = get_object_or_404(QnaReply, id=reply_id)
    qna_id = reply.comment.qna.id
    if request.method == 'POST' and request.user == reply.writer:
        reply.delete()
    return redirect('qnapage:qnadetail', qna_id)

def reply_likes(request, reply_id):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login_required.html')
    else:
        reply = get_object_or_404(QnaReply, id=reply_id)
        if request.user in reply.reply_like.all():
            reply.reply_like.remove(request.user)
            reply.reply_like_count -= 1
            reply.save()
        else:
            reply.reply_like.add(request.user)
            reply.reply_like_count += 1
            reply.save()
        return redirect('qnapage:qnadetail', reply.comment.qna.id)