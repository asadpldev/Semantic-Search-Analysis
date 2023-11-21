from django.db import models
from accounts.models import User
from accounts.mixins import TimeStampMixin
from django.db.models import Avg
from django.db.models import Count, Case, When, Value, CharField, F
class TVShow(TimeStampMixin):
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    views = models.IntegerField(default=0)

class Page(TimeStampMixin):
    name = models.CharField(max_length=100)
    link = models.URLField()
    details = models.TextField()
class Comment(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)
    comment_text = models.TextField()

class SentimentAnalysis(TimeStampMixin):
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE,blank= True,null=True)
    comment_text = models.ForeignKey(Comment, on_delete=models.CASCADE)
    analysis = models.CharField(max_length=100)
    
