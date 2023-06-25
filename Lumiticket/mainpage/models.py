from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    body = models.TextField()
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)
    report_count = models.PositiveIntegerField(default=0)

    # def __str__(self):
    #     return self.body[:20]
    def summary(self):
        return self.body[:40]

    def get_pub_date_date(self):
        return self.pub_date.date()

class Comment(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField()
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, null=False, blank=False, on_delete=models.CASCADE)

    def get_pub_date_date(self):
        return self.pub_date.date()

class Report(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['ticket', 'reporter']