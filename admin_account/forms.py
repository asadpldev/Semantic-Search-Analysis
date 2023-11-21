from django import forms
from .models import TVShow,Comment,Page

# Create your forms here.

class TVShowForm(forms.ModelForm):

	class Meta:
		model = TVShow
		fields = ("name", "description", "link")

class AddPageForm(forms.ModelForm):

	class Meta:
		model = Page
		fields = ("name", "link", "details")
  
class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ("user", "tv_show", "comment_text")
