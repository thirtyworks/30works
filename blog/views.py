from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
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
    now = timezone.now().strftime('%d-%m-%Y')
    day = (datetime.strptime(now, "%d-%m-%Y")-datetime.strptime(config_json.get('RELEASE_DATE', '01-04-2021'), "%d-%m-%Y")).days + 1
    if day > 30:
        day = 30
    if day < 1:
        day = 1 
    print('Its day:', day)
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
    

# Show all User/Artist posts on a current day
class PostsListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'  # <app>/<model>_<viewtype>.html
    # by default ListView will want to loop over a variable called `object_list`, but we called it `posts`
    # in the dictionary above
    # context_object_name = 'posts'
    # ordering = ['date_posted']  # oldest to newst
    # ordering = ['-date_posted'] # newest to oldest

    # queryset = Post.objects.all()
    # paginator = Paginator(queryset, paginate_by)

    def get_context_data(self,**kwargs):
        day_num = get_event_day()
        day = Day.objects.values_list('number', flat=True).get(number=day_num) 
        this_day = Day.objects.values_list('number', flat=True).get(number=self.kwargs.get('day')) 
        days_done = Day.objects.filter(number__range=(1, day_num)) 

        context = super(PostsListView, self).get_context_data(**kwargs)
        if this_day <= day:
            posts = Post.objects.filter(day__number=this_day, is_private=False).order_by('-datetime_posted')
        else:
            posts = None
        context['posts'] = posts
        context['days_done'] = days_done
        context['this_day'] = this_day
        return context



class PostDetailView(DetailView):
    model = Post

    def post(self, request, *args, **kwargs):
        name = request.POST.get("pk")
        # product = Product.objects.get(pk=pk)
        thepost = Post.objects.get(pk=name)

        if "rotate-left" in request.POST:

            # if the post is a picture upload
            if thepost.postpic:
                print('gunna rotate the post left ' + thepost.title)
                # open the image
                im = Image.open(thepost.postpic.path)

                im = im.rotate(90, expand=True)

                # save the image file
                im.save(thepost.postpic.path)
                print('SAVED THE IMAGEEEE')

        if "rotate-right" in request.POST:

            # if the post is a picture upload
            if thepost.postpic:
                print('gunna rotate the post right ' + thepost.title)
                # open the image
                im = Image.open(thepost.postpic.path)

                im = im.rotate(-90, expand=True)

                # save the image file
                im.save(thepost.postpic.path)
                print('SAVED THE IMAGEEEE')


        return redirect('post-detail', pk=thepost.id)

# Part of handling post form for PostCreateView
class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # get user from kwargs, but don't pass that kwarg to super
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ['title', 'url', 'postpic', 'postvideo', 'day', 'alt_text', 'is_private', 'anything_else']
        exclude = ('day',)

    def clean(self):
        day_num = get_event_day()
        # check that user has not already submitted today
        current_user = self.user  # from init
        # datetime_posted__date=timezone.now().date() saving here
        if Post.objects.filter(author=current_user, day__number=day_num).exists():
            # messages.error(current_user, 'You already submitted something today!')
            print('User {} was forbidden from posting again today'.format(self.user))
            raise forms.ValidationError("You already submitted something today")
        else:
            print('This is the users first submission ofthe day 1!!!!')

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
    # fields = ['title', 'content']
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

        print('HWLLOOOO is this a private post?? {}'.format(is_private))
        if is_private:
            try:
                email_from = settings.EMAIL_HOST_USER
                send_mail("Thanks for submitting for day {}".format(day.number), "Your work has been received!", email_from, [self.request.user.email])
            except SMTPResponseException as smtp_exception:
                print('Problem sending confirmation email!!')
                print(smtp_exception)


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


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'url']

    def form_valid(self, form):
        '''
        Assign the currently logged-in user as the author of this post
        '''
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        '''
        Check that the currently logged-in user is the author of the post attempting to be updated
        '''
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        '''
        Check that the currently logged-in user is the author of the post attempting to be updated
        '''
        post = self.get_object()
        return self.request.user == post.author

# Display user/artist profile with their works
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    # by default ListView will want to loop over a variable called `object_list`, but we called it `posts`
    # in the dictionary above
    context_object_name = 'posts'
    ordering = ['datetime_posted']  # oldest to newst

    # ordering = ['-date_posted'] # newest to oldest

    def get_context_data(self, *, object_list=None, **kwargs):
        user_profile = UserProfile.objects.get(acount_id=self.kwargs.get('acount_id')) 
        user = user_profile.user
        posts = Post.objects.filter(author=user).order_by('datetime_posted')
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['posts'] = posts
        context['user_details'] = user
        return context

    # def get_queryset(self):
    #     user_profile = UserProfile.objects.get(acount_id=self.kwargs.get('acount_id')) 
    #     user = user_profile.user
    #     return Post.objects.filter(author=user, is_private=False).order_by('datetime_posted')




def user_detail(request):
    # day = request.POST['day']
    # username = request.POST['username']
    day = request.GET['day']
    username = request.GET['username']
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        day_number = Day.objects.get(number=day)
        # mymodel.objects.filter(first_name__icontains="Foo", first_name__icontains="Bar")

        posts = Post.objects.filter(author=user, day=day_number)
    except:
        posts = {}
    return render(request, "blog/user_blogs.html", context={'posts': posts, 'users': user_profile})


# def countdown(request):
#     start_date = datetime.now()
#     live_date = datetime.strptime(config_json["live_date"], "%d-%m-%Y") 
#     remaining_days = abs((live_date - start_date).days)
#     return render(request, "countdown.html")

def success(request):
    return render(request, "blog/success.html")

