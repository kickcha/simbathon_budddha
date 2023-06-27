from django.urls import path
from .views import *

app_name = "qnapage"

urlpatterns = [
    path('qnalistrecent/', qnalistrecent, name="qnalistrecent"),
    path('qnalistpop/', qnalistpop, name="qnalistpop"),
    path('create/', create, name="create"),
    path('new/', new, name="new"),
    path('qnadetail/<int:id>/', qnadetail, name="qnadetail"),

    path('commentlikes/<int:comment_id>/', comment_likes, name="comment_likes"),
    path('commentdelete/<int:comment_id>', comment_delete, name ="comment_delete"),
    path('commentdelconfirm/<int:comment_id>', comment_delete_confirm, name ="comment_delete_confirm"),

    path('replycreate/<int:comment_id>/', reply_create, name="reply_create"),
    path('replydelete/<int:reply_id>/', reply_delete, name="reply_delete"),
    path('replydelconfirm/<int:reply_id>/', reply_delete_confirm, name="reply_delete_confirm"),
    path('replylikes/<int:reply_id>/', reply_likes, name="reply_likes"),
]