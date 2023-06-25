from django.urls import path, include
from .views import *

app_name = "mainpage"
urlpatterns = [
    path('', intropage, name="intropage"),
    path('loadingpage/', loadingpage, name="loadingpage"),
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('mainpage/', mainpage, name="mainpage"),
    path('qnapage/', include('qnapage.urls', namespace='qnapage')),
    path('<int:id>/', detail, name="detail"),
    path('likes/<int:ticket_id>', likes, name="likes"),
    path('delete/<int:id>', delete, name="delete"),
    path('ticketlistnew/', ticketlistnew, name="ticketlistnew"),
    path('ticketlistpop/', ticketlistpop, name="ticketlistpop"),
    path('report/<int:ticket_id>', report, name="report"),
]