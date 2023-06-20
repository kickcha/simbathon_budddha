from django.shortcuts import render, redirect, get_object_or_404
from .models import Qna
from django.utils import timezone

# Create your views here.
def create(request):
    if request.user.is_authenticated:
        new_qna = Qna()
        new_qna.title = request.POST['title']
        new_qna.writer = request.user
        new_qna.pub_date = timezone.now()
        new_qna.body = request.POST['body']
        new_qna.save()
        return redirect('qnapage:qnalistrecent')
    else:
        return redirect('accounts:login')

def new(request):
    return render(request, 'qnapage/newqna.html')

def qnalistrecent(request):
    qnas = Qna.objects.all()
    return render(request, 'qnapage/qnalistrecent.html', {'qnas':qnas})

def qnalistpop(request):
    qnas = Qna.objects.all()
    return render(request, 'qnapage/qnalistpop.html', {'qnas':qnas})

def qnadetail(request, id):
    qna = get_object_or_404(Qna, pk = id)
    return render(request, 'qnapage/qnadetail.html', {'qna':qna})