from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views  import PasswordResetView , PasswordResetConfirmView , PasswordResetCompleteView,PasswordResetDoneView
from .views import (
    AdminHomeView,
    TVShowUpdateView,
    TVShowListView
)

app_name = 'admin_accnt'
urlpatterns = [
    path("",AdminHomeView.as_view(),name='admin_home_page'),
    path("show/list/",TVShowListView.as_view(),name='tv_show_list'),
    path("update/<int:pk>",TVShowUpdateView.as_view(),name='update_tv_show'),
    

]