from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView
from .models import TVShow,Comment
from .forms import TVShowForm
from django.urls import reverse_lazy
from django.contrib import messages

class AdminHomeView(CreateView):
    template_name = 'admin_account/home.html'
    model = TVShow
    form_class = TVShowForm
    success_url = reverse_lazy('admin_accnt:tv_show_list') 
    
    def get(self,request, *args, **kwargs):
        form = self.form_class
        tv_shows = TVShow.objects.all()
        context = {
            'shows':tv_shows,
            'form': form
        }
        return render(request,self.template_name,context=context)
    
class TVShowListView(ListView):
    template_name = 'admin_account/tv_show_list.html'
    model = TVShow
    form_class = TVShowForm
    
    def get(self,request, *args, **kwargs):
        tv_shows = TVShow.objects.all()
        context = {
            'shows':tv_shows,
        }
        return render(request,self.template_name,context=context)
    
class TVShowUpdateView(UpdateView):
    model = TVShow
    fields = "__all__"
    template_name = 'admin_account/update_tvshow.html'
    success_url = reverse_lazy('admin_accnt:tv_show_list') 

