from django import forms
from .models import TVShow,Comment

# Create your forms here.

class TVShowForm(forms.ModelForm):

	class Meta:
		model = TVShow
		fields = ("name", "description", "link")

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ("user", "tv_show", "comment_text")
