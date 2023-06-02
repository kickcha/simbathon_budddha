from django.db import models

class Ticket(models.Model):
    nickname = models.CharField(max_length=30)
    pub_date = models.DateTimeField()
    body = models.TextField()