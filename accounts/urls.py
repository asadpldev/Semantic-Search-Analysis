from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views  import PasswordResetView , PasswordResetConfirmView , PasswordResetCompleteView,PasswordResetDoneView
from .views import (
     SignUpView,
     CustomLoginView,
     logout,
     ProfileView,
    UpdateUserView,
    #  ActivateAccount,
     password_reset_request,
     VerificationView,
     verificationEmailSent,
    #  TV SHOWS
    TVShowsView,
    TVShowDetailView


)

app_name = 'acnt'
urlpatterns = [
    path("",SignUpView.as_view(),name='signup_page'),
    path("login/",CustomLoginView.as_view(),name='login_page'),
    path("logout/",logout.as_view(),name='logout'),
    path("profile_view/",ProfileView.as_view(),name='profile-view'),
    path("profile_update/<int:id>/",UpdateUserView.as_view(), name='profile_update_page'),
# Password Reset
    path("password/reset", PasswordResetView.as_view(template_name = 'registration/password_reset.html') ,name="password_reste" ),
    path("password/reset_done", PasswordResetDoneView.as_view(template_name = 'registration/password_reset_done.html') ,name="password_reset_done" ),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_confirm.html') ,name="password_reset_confirm" ),
    path("password-reset-complete/", PasswordResetCompleteView.as_view(template_name = 'registration/password_reset_complete.html') ,name="password_reset_complete" ),
    path("password_reset", password_reset_request, name="password_reset"),
    # path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),

    path('verification_email_sent' , verificationEmailSent.as_view() , name="verificationmail"),
    # TV SHOWS
    path('tvshows/',TVShowsView.as_view(),name="tv_shows"),
    path('tvshow/comment/<int:pk>/',TVShowDetailView.as_view(),name="tv_show_detail")
    

]