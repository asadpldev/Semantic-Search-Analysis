from django.contrib import admin
from .models import TVShow,Comment,SentimentAnalysis,Page

admin.site.register(TVShow)
admin.site.register(Page)
admin.site.register(Comment)
admin.site.register(SentimentAnalysis)
