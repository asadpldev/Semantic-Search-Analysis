from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import View
from django.contrib.auth.models import auth
from django.contrib import messages
from .forms import SignUpForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token,analyze_sentiment
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from admin_account.models import TVShow,Comment,SentimentAnalysis


User = get_user_model()

class SignUpView(View):
    form_class = SignUpForm()
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        # username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user_obj = User.objects.filter(email=email).exists()
        if user_obj:
            messages.error(
                request,
                f"The e-mail address you entered is {email} in use, you can try another e-mail address, if the e-mail address belongs to you, you can try to log in..",
            )  
            return redirect("acnt:signup_page")
        if password1 == password2:
            if form.is_valid():
                form.save()
                return redirect("login")
            else:
                messages.error(request,form.errors)
                return redirect("acnt:signup_page")
        else:
            messages.error(request,"Password are not matching!")
            return redirect("acnt:signup_page")
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            messages.success(request, f"Your login appears to be done.")  
            return redirect("acnt:profile-view")
        context = {"is_header": "header",
            "form":SignUpForm()
        }
        return render(request, "registration/register.html", context=context)
        
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')

class verificationEmailSent(View):
   def get(self , request, *args , **kwargs):
       return render(request, 'emails/verification_email_sent.html')

class logout(LoginRequiredMixin , View):
    def get(self,request,*args,**kwargs):
        auth.logout(request)
        return redirect("login")

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "registration/reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})

class ProfileView(LoginRequiredMixin,View):
    
    def get(self,request,*args,**kwargs):
        return render(request,'user/profile.html')

class UpdateUserView(LoginRequiredMixin,View):
    
    def post(self,request,*args,**kwargs):

        first_name   = request.POST.get("first_name") 
        last_name    = request.POST.get("last_name") 
        user_name    = request.POST.get("user_name") 
        # email        = request.POST.get("email") 
        date_of_birth  = request.POST.get("date_of_birth")
        # profile_image  = request.FILES["add_profile_image"]
       
        user  = get_object_or_404(User,id=request.user.id)
       
        if 'add_profile_image' in request.FILES:
            # profile = user.profile
            user.profile_pic = request.FILES['add_profile_image']
            messages.success (request,"Profile pic has been updated")
            user.save()
            return redirect ("acnt:profile-view")
        if 'first_name' and 'last_name' in request.POST:
            user.first_name = first_name
            user.last_name  = last_name
            user.username = user_name
            # user.date_of_birth  = date_of_birth
            user.save()
            messages.success (request,"User has been updated")
            return redirect ("acnt:profile-view")
        else:
            messages.success (request,"an error occured! :( ")
            return redirect ("acnt:profile-view")

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  
    success_url = reverse_lazy('acnt:profile-view') 

    def get_success_url(self):
        user = self.request.user
        if user.is_admin:
            return reverse_lazy('admin_accnt:admin_dashboard')  # Replace 'admin_dashboard' with your admin dashboard URL name
        return self.success_url

    def form_valid(self, form):
        user = form.get_user()
        if user.is_active:
            print("Custom login form")
            # self.request.session['some_data'] = 'something'  # You can add more custom logic here
            return super().form_valid(form)
        return redirect('acnt:signup_page')  # Redirect to an inactive account page

class TVShowsView(View):
     
    def get(self,request, *args, **kwargs):
        tv_shows = TVShow.objects.all()

        context = {
            'shows':tv_shows,
        }
        return render(request,"user/tv_show_list.html",context=context)

class TVShowDetailView(LoginRequiredMixin,View):
    template_name = 'user/add_comment.html'
    model = Comment
    form_class = CommentForm
    
    def get(self,request, *args, **kwargs):
        form = self.form_class
        tv_show = TVShow.objects.get(id=self.kwargs.get("pk"))
        comment_obj = Comment.objects.filter(user=request.user,tv_show=tv_show).first()        
        comments = Comment.objects.filter(tv_show = tv_show).order_by("-id") 
        context = {
            'show':tv_show,
            'form': form,
            'comment': comment_obj,
            'comments':comments
        }
        return render(request,self.template_name,context=context)
    
    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST)
        tv_show_id=self.kwargs.get("pk")
        tv_show = TVShow.objects.get(id=self.kwargs.get("pk"))        
        if form.is_valid():
            form = form.save(commit=False)
            form.tv_show = tv_show
            form.user = request.user
            form.save()
            # Statement Analysis
            statement_analysis = analyze_sentiment(form.comment_text)
            analysis_obj = SentimentAnalysis.objects.create(tv_show=tv_show,comment_text = form,analysis = statement_analysis)
            messages.success(request,"Comment is added successfully!")
            return redirect("acnt:tv_show_detail",pk=tv_show_id)

        messages.error(request,form.errors)
        return redirect("acnt:tv_show_detail",pk=tv_show_id)
