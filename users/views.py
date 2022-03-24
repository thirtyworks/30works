from distutils.log import error
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import MyUserCreationForm, UserUpdateForm, UserProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import Day
from django.forms import ValidationError
from django.contrib.auth.models import User
import copy
from django.db.models.functions import Lower

# Create your views here.
def register(request):
    days = Day.objects.all()
    if len(days) < 1:
        if request.method == 'POST':
            # form = UserCreationForm(request.POST)
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account created for {}'.format(username))
                # and send the user back to homepage
                return redirect('home')
                # and send user to login page
                # return redirect('login')
        else:
            # form = UserCreationForm()
            form = MyUserCreationForm()
        return render(request, 'users/register.html', {'form': form})
    else:
        return redirect('home')


class MyUserUpdateForm(UserUpdateForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request') # get request from kwargs, but don't pass that kwarg to super
        self.current_user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

# Update account profile info
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = MyUserUpdateForm(request.POST, instance=request.user, request=request)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)
        print(u_form.error_class.as_data)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid character in first_name or last_name, please use only alphanumeric characters and underscores')

    else:
        print('NOT a POST method')
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.user_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/edit-profile.html', context)

# Get all users/artists except current logged in user
def artists(request):
    users = User.objects.filter().exclude(username=request.user.id).order_by(Lower('first_name'))
    return render(request, 'users/artists.html', context={'artists':users})
    