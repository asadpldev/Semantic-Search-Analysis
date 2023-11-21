from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User
from admin_account.models import Comment
from django_countries.fields import CountryField

class AgeField(forms.CharField):
    def clean(self, value):
        # Check if the value matches the expected date format (YYYY-MM-DD)
        from datetime import datetime
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise forms.ValidationError('Please enter a valid date in YYYY-MM-DD format.')
        return value
    

class SignUpForm(UserCreationForm):
	username = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	age = AgeField(required=True, label='Date of Birth (YYYY-MM-DD)')
	# age = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, 2023))) 
	location = CountryField().formfield() 

	class Meta:
		model = User
		fields = ("username","age","location", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(SignUpForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	def __init__(self, *args, **kwargs):
			super(SignUpForm,self).__init__(*args, **kwargs)
			self.fields['username'].widget.attrs['placeholder']= 'Enter your username' 
			self.fields['age'].widget.attrs['placeholder']= 'Enter your age' 
			self.fields['location'].widget.attrs['placeholder']= 'Enter your location' 
			self.fields['email'].widget.attrs['placeholder']= 'Enter your email' 
			self.fields['password1'].widget.attrs['placeholder']= 'Enter your password'
			self.fields['password2'].widget.attrs['placeholder']= 'Confirm password'
class UpdateUserForm(forms.ModelForm):


	class Meta:
		model = User
		fields = ("first_name", "last_name", "gender", "age","location")
		def __init__(self, *args, **kwargs):
			super(UpdateUserForm,self).__init__(*args, **kwargs)
			self.fields['first_name'].widget.attrs['class']= 'form-control' 
			self.fields['last_name'].widget.attrs['class']= 'form-control' 
			self.fields['age'].widget.attrs['class']= 'form-control' 
			self.fields['about'].widget.attrs['class']= 'form-control' 
			self.fields['location'].widget.attrs['class']= 'form-control'

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ("comment_text",)
		labels = {
            'comment_text': 'Add your comment here',
        }