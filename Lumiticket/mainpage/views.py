from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Comment, Report
from django.utils import timezone
from qnapage import *
from accounts import *
from django.db.models import Count, F
from django.core.paginator import Paginator
# loading page관련 메서드
from django.template import loader
import time
import re

def mainpage(request): 
    tickets = Ticket.objects.order_by('-like_count')[:2]
    return render(request, 'mainpage/mainpage.html', {'tickets': tickets})

def report(request, ticket_id):
    if request.user.is_authenticated:
        ticket = get_object_or_404(Ticket, id=ticket_id)

        if request.method == 'POST':
            reporter = request.user
        else:
            return redirect('mainpage:detail', id=ticket_id)

        # 이미 신고한 경우 처리
        if Report.objects.filter(ticket=ticket, reporter=request.user).exists():
            return redirect('mainpage:detail', id=ticket_id)

        # 새로운 신고 생성
        report = Report.objects.create(ticket=ticket, reporter=reporter)

        # 추가로 신고 처리 로직 구현
        if ticket.report_count >= 3:
            # 게시글을 보류 상태로 변경
            ticket.status = '보류'
        else:
            ticket.report_count += 1
        ticket.save()
            # 또는 게시글을 삭제할 수도 있습니다.
            # ticket.delete()

        return redirect('mainpage:detail', id=ticket_id)

    return redirect('mainpage:detail', id=ticket_id)

def detail(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    ticket.pub_date = ticket.pub_date.date()

    if Report.objects.filter(ticket=ticket).count() >= 3:
        ticket.status = '보류'
        ticket.save()

    return render(request, 'mainpage/detail.html',{'ticket':ticket})

def intropage(request):
    return render(request, 'mainpage/intropage.html')

def loadingpage(request):
    return render(request, 'mainpage/loadingpage.html')

def filter_profanity(text):
    profanities = ['시발', '씨발', '좆', '새끼', '썅', '씨팔', '시팔', '쒸발', 'ㅅㅂ', 'ㅆㅂ', '지랄', 'ㅈㄹ', '18년', 
    '18놈', '18새끼', '강간', '개가튼년', '개가튼뇬', '개같은년', '개걸레', '개넘', '개년', '개놈', '개새', '개쓰래기', '개쓰레기',
    '개씨발', '개씨블', '개자식', '개자지', '개잡년', '개젓가튼넘', '개좆', '개지랄', '걔잡년', '거시기', '걸래년', '걸레같은년',
    '걸레년', '걸레핀년', '게부럴', '게세끼', '게이', '게새끼', '게늠', '게자식', '게지랄놈', '고환', '귀두', '깨쌔끼', '내꺼빨아',
    '내꺼핧아', '너거애비', '니애미', '니애뷔', '니애비', '니할애비', '니미', '닳은년', '돈새끼', '돌은넘', '돌은새끼', '딸딸이',
    '띠발뇬', '띠팔', '띠펄', '띠풀', '띠벌', '띠벨', '띠빌', '막간년', '막대쑤셔줘', '막대핧아줘', '맛간년', '맛없는년', '맛이간년',
    '미친구녕', '미친구멍', '미친넘', '미친년', '미친놈', '미친눔', '미친새끼', '미친씨부랄', '미튄', '미티넘', '미틴', '미틴넘', '미틴년', 
    '미틴놈', '미틴것', '백보지', '버지구녕', '버지구멍', '버지냄새', '버지따먹기', '버지뚫어', '버지뜨더', '버지물마셔', '버지벌려', '버지벌료'
    , '버지빨아', '버지빨어', '버지썰어', '버지쑤셔', '버지털', '버지핧아', '버짓물', '버짓물마셔', '벌창같은년', '벵신', '병닥', '병딱'
    , '병신', '보쥐', '보지', '보지핧어', '보짓물', '보짓물마셔', '봉알', '부랄', '불알', '붕알', '붜지', '뷩딱', '븅쉰', '븅신'
    , '빙띤', '빙신', '빠가십새', '빠가씹새', '빠구리', '빠굴이', '뽕알', '뽀지', '뼝신', '사까시', '상년', '새꺄', '새뀌', '새끼'
    , '색갸', '색끼', '색스', '색키', '샤발', '써글', '써글년', '성교', '성폭행', '세꺄', '세끼', '섹스', '섹스하자', '섹스해', '섹쓰'
    , '섹히', '수셔', '쑤셔', '쉐끼', '쉑갸', '쉑쓰', '쉬발', '쉬방', '쉬밸년', '쉬벌', '쉬불', '쉬붕', '쉬빨', '쉬이발', '쉬이방', '쉬이벌'
    , '쉬이불', '쉬이붕', '쉬이빨', '쉬이팔', '쉬이펄', '쉬이풀', '쉬팔', '쉬펄', '쉬풀', '쉽쌔', '시댕', '시발', '시발년', '시발놈'
    , '시밸', '시벌', '시불', '시붕', '시이발', '시이벌', '시이불', '시이붕', '시이팔', '시이펄', '시이풀', '시팍새끼', '시팔'
    , '시팔넘', '시팔년', '시팔놈', '시팔새끼', '시펄', '십8', '십때끼', '십떼끼', '십버지', '십부랄', '십부럴', '십새', '십세이'
    , '십셰리', '십쉐', '십자석', '십자슥', '십지랄', '십창녀', '십창', '십탱', '십탱구리', '십탱굴이', '십팔새끼', 'ㅆㅂㄹㅁ', 'ㅆㅂㄻ'
    , '쌍년', '쌍놈', '쌍눔', '쌍보지', '쌔끼', '쌔리', '쌕스', '쌕쓰', '쓉새', '쓰바새끼', '쓰브랄쉽세', '씌발', '씌팔', '씨가랭넘', '씨가랭년'
    , '씨가랭놈', '씨발', '씨발년', '씨발롬', '씨발병신', '씨방새', '씨방세', '씨밸', '씨뱅가리', '씨벌', '씨벌년', '씨벌쉐이', '씨부랄', '씨부럴'
    , '씨불', '씨불알', '씨붕', '씨브럴', '씨블', '씨블년', '씨븡새끼', '씨빨', '씨이발', '씨이벌', '씨이불', '씨이붕', '씨이팔'
    , '씨파넘', '씨팍새끼', '씨팍세끼', '씨팔', '씨펄', '씨퐁넘', '씨퐁뇬', '씨퐁보지', '씨퐁자지', '씹년', '씹물', '씹미랄', '씹버지', '씹보지'
    , '씹부랄', '씹브랄', '씹빵구', '씹뽀지', '씹새', '씹새끼', '씹세', '씹쌔끼', '씹자석', '씹자슥', '씹자지', '씹지랄', '씹창', '씹창녀', '씹탱', '씹탱굴이'
    , '씹탱이', '씹팔', '아가리', '애무', '애미', '애미랄', '애미보지', '애미씨뱅', '애미자지', '애미잡년', '애자', '양아치', '어미강간', '어미따먹자'
    , '어미쑤시자', '엄창', '에미', '에비', '염병', '염병할', '염뵹', '엿먹어라', '오랄', '오르가즘', '왕버지', '왕자지', '왕털보지', '왕털자지'
    , '왕털잠지', '유두', '유두빨어', '유두핧어', '유방', '유방만져', '유방빨아', '유방주물럭', '유방쪼물딱', '유방쪼물럭', '유방핧아', '유방핧어'
    , '육갑', '이년', '자기핧아', '자지', '자지구녕', '자지구멍', '자지꽂아', '자지넣자', '자지뜨더', '자지뜯어', '자지박어', '자지빨아', '자지빨아줘', '자지빨어'
    , '자지쑤셔', '자지쓰레기', '자지정개', '자지짤라', '자지털', '자지핧아', '자지핧아줘', '자지핧어', '작은보지', '잠지', '잠지뚫어', '잠지물마셔', '잠지털', '잠짓물마셔'
    , '잡년', '잡놈', '저년', '점물', '젓가튼', '젓가튼쉐이', '젓같내', '젓같은', '젓까', '젓나', '젓떠', '젓마무리', '젓만이', '젓물', '젓물냄새', '젓밥'
    , '정액마셔', '정액먹어', '정액발사', '정액짜', '정액핧아', '정자마셔', '정자먹어', '정자핧아', '젖같은', '젖까', '조개넓은년', '조개따조'
    , '조개마셔줘', '조개벌려조', '조개속물', '조개쑤셔줘', '조개핧아줘', '조까', '조또', '족같내', '족까', '족까내', '존나', '존나게'
    , '존니', '졸라', '좀마니', '좀물', '좀쓰레기', '좁빠라라', '좃가튼뇬', '좃간년', '좃까', '좃까리', '좃깟네', '좃냄새', '좃넘', '좃대가리'
    , '좃도', '좃또', '좃만아', '좃만이', '좃만한것', '좃만한쉐이', '좃물', '좃물냄새', '좃보지', '좃부랄', '좃빠구리', '좃빠네', '좃빠라라', '좃털'
    , '좆같은놈', '좆같은새끼', '좆까', '좆까라', '좆나', '좆년', '좆도', '좆만아', '좆만한년', '좆만한놈', '좆만한새끼', '좆먹어'
    , '좆물', '좆밥', '좆빨아', '좆새끼', '좆털', '좋만한것', '주글년', '주길년', '쥐랄', '지랄', '지랼', '지럴', '지뢀', '쪼까튼', '쪼다', '쪼다새끼'
    , '찌랄', '찌질이', '창남', '창녀', '창녀버지', '창년', '처먹고', '처먹을', '쳐먹고', '쳐쑤셔박어', '촌씨브라리', '촌씨브랑이', '촌씨브랭이', '크리토리스'
    , '큰보지', '클리토리스', '페니스', '항문수셔', '항문쑤셔', '허버리년', '허벌년', '허벌보지', '허벌자식', '허벌자지', '호냥년', '호로'
    , '호로새끼', '호로자슥', '호로자식', '호로짜식', '호루자슥', '호모', '호졉', '호좁', '후라덜넘', '후장', '후장꽂아', '후장뚫어', 'bitch', 'fuck'
    , 'fuckyou', 'nflavor', 'penis', 'pennis', 'pussy', 'sex']

    for profanity in profanities:
        pattern = r'\b' + profanity + r'\b'
        text = re.sub(pattern, '*' * len(profanity), text, flags=re.IGNORECASE)
    return text

def new(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login_required.html')
    else:
        return render(request, 'mainpage/new.html')

def create(request):  # 티켓 적는 함수
    if request.user.is_authenticated:
        new_ticket = Ticket()
        new_ticket.writer = request.user
        new_ticket.pub_date = timezone.now()

        body = request.POST['body']  # 입력된 티켓 내용
        filtered_body = filter_profanity(body)  # 욕설 필터링 적용

        new_ticket.body = filtered_body
        new_ticket.save()

        return redirect('mainpage:detail', id=new_ticket.id)
    else:
        return redirect('accounts:login')


def likes(request, ticket_id):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login_required.html')
    else:
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
