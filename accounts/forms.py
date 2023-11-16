from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User
from admin_account.models import Comment

# Create your forms here.

class SignUpForm(UserCreationForm):
	email = forms.EmailField(required=True)
	username = forms.CharField(required=True)
 

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(SignUpForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
class UpdateUserForm(forms.ModelForm):


	class Meta:
		model = User
		fields = ("first_name", "last_name", "description", "about","location")
		def __init__(self, *args, **kwargs):
			super(UpdateUserForm,self).__init__(*args, **kwargs)
			self.fields['first_name'].widget.attrs['class']= 'form-control' 
			self.fields['last_name'].widget.attrs['class']= 'form-control' 
			self.fields['description'].widget.attrs['class']= 'form-control' 
			self.fields['about'].widget.attrs['class']= 'form-control' 
			self.fields['location'].widget.attrs['class']= 'form-control'

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ("comment_text",)
		labels = {
            'comment_text': 'Add your comment here',
        }