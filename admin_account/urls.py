from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views  import PasswordResetView , PasswordResetConfirmView , PasswordResetCompleteView,PasswordResetDoneView
from .views import (
    AdminDashboardView,
    AdminHomeView,
    AdminAddPageView,
    PageUpdateView,
    TVShowUpdateView,
    TVShowListView,
    get_sentiment_data
)

app_name = 'admin_accnt'
urlpatterns = [
    path("",AdminDashboardView.as_view(),name='admin_dashboard'),
    path("add/tv_show/",AdminHomeView.as_view(),name='admin_home_page'),
    path("add/page/",AdminAddPageView.as_view(),name='admin_add_page'),
    path("update/page/<int:pk>",PageUpdateView.as_view(),name='update_page'),
    path("show/list/",TVShowListView.as_view(),name='tv_show_list'),
    path("update/<int:pk>",TVShowUpdateView.as_view(),name='update_tv_show'),
    path("get_sentiment_data/",get_sentiment_data,name='get_sentiment_data'),
    

]