from django.contrib import admin
from .models import TVShow,Comment,SentimentAnalysis

admin.site.register(TVShow)
admin.site.register(Comment)
admin.site.register(SentimentAnalysis)
