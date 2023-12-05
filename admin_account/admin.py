from django.contrib import admin
from .models import TVShow,Comment,SentimentAnalysis,Page

class TVShowAdmin(admin.ModelAdmin):
    model = TVShow
    list_display = ["id",'name', 'description', 'link', 'views']

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ["id",'user', 'tv_show', 'comment_text']

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ["id",'user', 'tv_show', 'comment_text','get_analysis']
    @admin.display(ordering='book__author', description='Author')
    def get_analysis(self, obj):
        obj = SentimentAnalysis.objects.get(id=obj.id)
        return obj.analysis

admin.site.register(TVShow,TVShowAdmin)
admin.site.register(Page)
admin.site.register(Comment,CommentAdmin)
admin.site.register(SentimentAnalysis)
