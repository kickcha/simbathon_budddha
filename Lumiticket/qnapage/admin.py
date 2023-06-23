from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Qna)
admin.site.register(QnaComment)
admin.site.register(QnaReply)