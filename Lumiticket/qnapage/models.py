from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Qna(models.Model):
    title = models.CharField(max_length = 200)
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    body = models.TextField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
class QnaComment(models.Model):
    contenct = models. TextField()
    pub_date = models.DateTimeField()
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    qna = models. ForeignKey(Qna, null=False, blank=False, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null = True, related_name='reply')