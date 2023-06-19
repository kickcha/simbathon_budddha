from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    body = models.TextField()

    def __str__(self):
        return self.body[:20]