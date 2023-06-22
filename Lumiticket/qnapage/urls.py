from django.urls import path
from .views import *

app_name = "qnapage"

urlpatterns = [
    path('qnalistrecent/', qnalistrecent, name="qnalistrecent"),
    path('qnalistpop/', qnalistpop, name="qnalistpop"),
    path('create/', create, name="create"),
    path('new/', new, name="new"),
    path('qnadetail/<int:id>/', qnadetail, name="qnadetail"),
    # path('comment/<int:qna_id>/<int:comment_id>', comment, name="comment"),
    path('commentlikes/<int:comment_id>/', comment_likes, name="comment_likes"),
    path('commentedit/<int:comment_id>', comment_edit, name ="comment_edit"),
    path('commentdelete/<int:comment_id>', comment_delete, name ="comment_delete"),
]