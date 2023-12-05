from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,View
from .models import TVShow,Comment,SentimentAnalysis,Page
from .forms import TVShowForm,AddPageForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Case, When, Value, CharField
from django.contrib.auth import get_user_model
User = get_user_model()
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

def get_age_data(request, tv_show_id):
    # Get the TV show
    tv_show = TVShow.objects.get(pk=tv_show_id)

    # Get ages of users who commented on this TV show
    user_ages = Comment.objects.filter(tv_show=tv_show).values_list('user__age', flat=True)

    # Process the data (e.g., count users in different age groups)
    age_groups = {
        '0-20': 0,
        '21-40': 0,
        '41-60': 0,
        '61+': 0,
    }
    for age in user_ages:
        if int(age) <= 20:
            age_groups['0-20'] += 1
        elif int(age) <= 40:
            age_groups['21-40'] += 1
        elif int(age) <= 60:
            age_groups['41-60'] += 1
        else:
            age_groups['61+'] += 1

    # Prepare data for the chart
    labels = list(age_groups.keys())
    data = list(age_groups.values())

    # Return data as JSON response
    chart_data = {
        'labels': labels,
        'data': data,
    }
    return JsonResponse(chart_data)

def get_gender_data(request, tv_show_id):
    # Get the TV show
    tv_show = TVShow.objects.get(pk=tv_show_id)

    # Get genders of users who commented on this TV show
    user_genders = Comment.objects.filter(tv_show=tv_show).values('user__gender')
    # Process the data to count genders
    gender_counts = user_genders.annotate(
        gender_type=Case(
            When(user__gender='male', then=Value('male')),
            When(user__gender='female', then=Value('female')),
            default=Value('other'),
            output_field=CharField(),
        )
    ).values('gender_type').annotate(total_count=Count('gender_type'))
    print("Gender count:",gender_counts)
    # Prepare data for the chart
    labels = [gender['gender_type'] for gender in gender_counts]
    gender_data = [gender['total_count'] for gender in gender_counts]

    # Return data as JSON response
    chart_data = {
        'labels': labels,
        'gender_data': gender_data,
    }
    return JsonResponse(chart_data)

def get_location_data(request, tv_show_id):
    # Get the TV show
    tv_show = TVShow.objects.get(pk=tv_show_id)

    # Get locations of users who commented on this TV show
    user_locations = User.objects.filter(
        comment__tv_show=tv_show
    ).values('location').annotate(total_count=Count('location'))
    print("Location:",user_locations)
    # Prepare data for the chart
    labels = [location['location'] for location in user_locations]
    location_data = [location['total_count'] for location in user_locations]

    # Return data as JSON response
    chart_data = {
        'labels': labels,
        'location_data': location_data,
    }
    return JsonResponse(chart_data)

def get_sentiment_data(request, tv_show_id):
    # Get the TV show
    tv_show = TVShow.objects.get(pk=tv_show_id)

    # Get sentiment analysis for comments related to the TV show
    comment_sentiments = SentimentAnalysis.objects.filter(
        tv_show=tv_show
    ).values('analysis').annotate(total_count=Count('analysis'))

    # Prepare data for the chart
    labels = [sentiment['analysis'] for sentiment in comment_sentiments]
    sentiment_data = [sentiment['total_count'] for sentiment in comment_sentiments]

    # Return data as JSON response
    chart_data = {
        'labels': labels,
        'sentiment_data': sentiment_data,
    }
    return JsonResponse(chart_data)

def get_review_sentiment_data(request, tv_show_id):
    # Get the TV show
    tv_show = TVShow.objects.get(pk=tv_show_id)

    # Get reviews related to the TV show
    review_sentiments = SentimentAnalysis.objects.filter(
        tv_show=tv_show
    ).values('analysis').annotate(total_count=Count('analysis'))

    # Prepare data for the chart
    review_labels = [review['analysis'] for review in review_sentiments]
    review_sentiment_data = [review['total_count'] for review in review_sentiments]

    # Return data as JSON response
    chart_data = {
        'review_labels': review_labels,
        'review_sentiment_data': review_sentiment_data,
    }
    return JsonResponse(chart_data)