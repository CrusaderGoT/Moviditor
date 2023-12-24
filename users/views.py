from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import Http404
from django.contrib.auth.models import User
from . models import Profile
from .forms import ProfileForm
from django.contrib import messages
# Create your views here.
t_path = 'C:\\Users\\DELL\\Documents\\Python_Files\\Moviditor\\users\\templates\\registration'

def sign_up(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            new_user = form.save(commit=False)
            new_user.email = email
            new_user.username = username
            new_user.password1 = password1
            new_user.password2 = password2
            new_user.save()
            login(request, new_user)
            return redirect('users:create-profile')
    context = {'form': form}
    return render(request, f'{t_path}\\sign_up.html', context)

def create_profile(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        messages.warning(request, 'You must have an account first, in order to create a Profile.')
        return redirect('users:sign-up')
    else:
        user = user
        if request.method != 'POST':
            form = ProfileForm()
        else:
            form = ProfileForm(data=request.POST, files=request.FILES)
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            # confirm the mime type of the picture later
            new_profile.save()
            return redirect('users:profile', user.username)
        context = {'user': user, 'form': form}
        return render(request, f'{t_path}\\create_profile.html', context)

def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    if request.method != 'POST' and request.user == user:
        context = {'user': user, 'profile': profile}
        return render(request, f'{t_path}\\profile.html', context)
    else:
        raise Http404()