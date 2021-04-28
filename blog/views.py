from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Post, Day
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, datetime
import os
import json
from django.db.models import Q
from users.models import UserProfile
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from PIL import Image
from smtplib import SMTPDataError, SMTPResponseException
from django.urls import reverse
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, '30works.json'), 'r') as f:
    config_json = json.load(f)

def get_event_day():
    now = timezone.localtime().strftime('%d-%m-%Y, %X')
    # datetime.strptime('01-04-2021, 00:20:00', "%d-%m-%Y, %X") 
    day = (datetime.strptime(now, "%d-%m-%Y, %X") - datetime.strptime(config_json.get('RELEASE_DATE', '01-04-2021, 00:20:00'), "%d-%m-%Y, %X")).days + 1
    if day > 30:
        day = 30
    if day < 1:
        day = 1 
    print('Its day:', day)
    return day

def get_event_day_with_limit():
    now = timezone.localtime().strftime('%d-%m-%Y, %X')
    day = (datetime.strptime(now, "%d-%m-%Y, %X") - datetime.strptime(config_json.get('RELEASE_DATE', '01-04-2021, 00:20:00'), "%d-%m-%Y, %X")).days + 1
    if day > 30:
        day = 31
    if day < 1:
        day = 1 
    return day

def get_brief():
    df = pd.read_csv(os.path.join(BASE_DIR, 'briefs.csv'))
    day = get_event_day()
    brief_day = df['BRIEFS'][day-1]
    return brief_day

def home(request):
    if len(Day.objects.all()) != 30:
        for i in range(1,31):
            try:
                Day.objects.create(number=i)
                print('Day {} added!'.format(i))
            except:
                print('Day {} already exists'.format(i))
            Day.save
        print('All 30 days now exist!')
    else:
        print('All 30 days already exist')
    
    latest_day = Day.objects.last()
    day_num = get_event_day()
    days_done = Day.objects.filter(number__range=(1, day_num)).order_by('-number')
    # current date - starting date
    return render(request, "home.html", context={'days_done': days_done})

def about(request):
    return render(request, "about.html", context={'title': 'About 30Works'})
    
def event_day(request):
    day = get_event_day()
    return HttpResponseRedirect(reverse('artist-posts', kwargs={'day': day}))


# Show all User/Artist posts on a current day
class PostsListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html' 
    paginate_by = 15
    context_object_name = 'posts'

    def get_queryset(self):
        this_day = Day.objects.values_list('number', flat=True).get(number=self.kwargs.get('day'))
        return Post.objects.filter(day__number=this_day, is_private=False).order_by('-datetime_posted')

    def get_context_data(self,**kwargs):
        day_num = get_event_day()
        day = Day.objects.values_list('number', flat=True).get(number=day_num) 
        this_day = Day.objects.values_list('number', flat=True).get(number=self.kwargs.get('day')) 
        days_done = Day.objects.filter(number__range=(1, day_num)) 

        context = super(PostsListView, self).get_context_data(**kwargs) 
    
        context['days_done'] = days_done
        context['this_day'] = this_day
        return context


# Part of handling post form for PostCreateView
class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # get user from kwargs, but don't pass that kwarg to super
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ['title', 'url', 'postpic', 'postvideo', 'post_text', 'day', 'alt_text', 'is_private', 'anything_else']
        exclude = ('day',)

    def clean(self):
        day_num = get_event_day()
        # check that user has not already submitted today
        current_user = self.user.id # from init
    
        if Post.objects.filter(author__id=current_user, day__number=day_num, author__is_staff=False).exists():
            # messages.error(current_user, 'You already submitted something today!')
            print('User {} was forbidden from posting again today'.format(self.user))
            raise forms.ValidationError("You already submitted a post today")
        else:
            print('This is the users first submission of the day !!')

        current_user_profile = UserProfile.objects.get(user=current_user)
        if current_user_profile.blocked:
            print('User us blocked!!!!!!!!!!!!!!!!!!!')
            raise forms.ValidationError("Sorry, you are not allowed to submit anymore.")
        else:
            print('USer is not blocked')
        super().clean()

# User add post of the day
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    
    def get_form_kwargs(self):
        """ add user to form kwargs """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
     
    def form_valid(self, form):
        '''
        Assign the currently logged-in user as the author of this post
        '''
        form.instance.author = self.request.user
        today = date.today()
        # day = Day.objects.get(date_posted__date=today)
        day = Day.objects.get(number=get_event_day())
        form.instance.day = day

        is_private = form.instance.is_private

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        day_num = get_event_day()
        # days_done = Day.objects.filter(number__range=(1, day_num)) 
        # this_day = Day.objects.values_list('number', flat=True).get(number=self.kwargs.get('day')) 
        
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['brief_day'] = get_brief()
        context['latest_day'] = Day.objects.values_list('number', flat=True).get(number=day_num) 
        return context

    def get_success_url(self):
        return reverse('success')

# Update user post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'url', 'postpic', 'postvideo', 'post_text', 'alt_text', 'is_private', 'anything_else']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        '''
        Assign the currently logged-in user as the author of this post
        '''
        form.instance.author = self.request.user
      
        print(form.instance.postpic)
   
        return super().form_valid(form)

    def test_func(self):
        '''
        Check that the currently logged-in user is the author of the post attempting to be updated
        '''
        post = self.get_object()
        print(get_event_day() == post.day.number) #todo: add to condition
        return self.request.user == post.author 

    def get_success_url(self):
        messages.success(self.request, 'Your post has been updated')
        return self.request.path_info

# Delete user post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        '''
        Check that the currently logged-in user is the author of the post attempting to be updated
        '''
        post = self.get_object()
        print(post.author.user_profile.acount_id)
        return self.request.user == post.author
    
    def get_success_url(self):
        post = self.get_object()
        messages.success(self.request, 'Your post has successfully been deleted')
        return reverse('user-posts', args=([post.author.user_profile.acount_id]))

# Display user/artist profile with their works
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' 
    context_object_name = 'posts'
    paginate_by = 30

    def get_queryset(self):
        user_profile = UserProfile.objects.get(acount_id=self.kwargs.get('acount_id')) 
        user = user_profile.user
        return Post.objects.filter(author=user).order_by('-day')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        user_profile = UserProfile.objects.get(acount_id=self.kwargs.get('acount_id')) 
        user = user_profile.user
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['this_day'] = get_event_day_with_limit()
        context['user_details'] = user
        return context

# Success page
def success(request):
    return render(request, "success.html")

def profile(request):
    user = UserProfile.objects.get(user=request.user.id)
    return HttpResponseRedirect(reverse('profile'))
