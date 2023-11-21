from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,View
from .models import TVShow,Comment,SentimentAnalysis,Page
from .forms import TVShowForm,AddPageForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse

class AdminDashboardView(View):
    template_name = 'admin_account/dashboard.html'
 
    def get(self,request, *args, **kwargs):
        # form = self.form_class
        analysis = SentimentAnalysis.objects.filter()
        tv_shows = TVShow.objects.all()
        context = {
            'shows':tv_shows,
            # 'form': form
        }
        return render(request,self.template_name,context=context)

def get_sentiment_data(request):
    # Fetching data for sentiment analysis based on user age, gender, location, and sentiment
    sentiments_data = SentimentAnalysis.objects.values('analysis').annotate(count=Count('analysis'))

    # Processing the data into separate lists for chart rendering
    xValues = [item['analysis'] for item in sentiments_data]
    yValues = [item['count'] for item in sentiments_data]

    # Returning the data as JSON response
    chart_data = {
        'labels': xValues,
        'data': yValues,
    }
    return JsonResponse(chart_data)
    
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

class AdminAddPageView(CreateView):
    template_name = 'admin_account/add_page.html'
    model = Page
    form_class = AddPageForm
    success_url = reverse_lazy('admin_accnt:admin_add_page')
    
    def get(self,request, *args, **kwargs):
        form = self.form_class
        pages = Page.objects.all()
        context = {
            'pages':pages,
            'form': form
        }
        return render(request,self.template_name,context=context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Page created successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
            
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
    fields = ['name','description','link']
    template_name = 'admin_account/update_tvshow.html'
    success_url = reverse_lazy('admin_accnt:tv_show_list') 

class PageUpdateView(UpdateView):
    model = Page
    fields = "__all__"
    template_name = 'admin_account/update_page.html'
    success_url = reverse_lazy('admin_accnt:admin_add_page')

    def form_valid(self, form):
        messages.success(self.request, 'Page updated successfully!')
        return super().form_valid(form) 
    