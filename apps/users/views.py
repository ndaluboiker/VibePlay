from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from apps.videos.models import Video
from .forms import MyUserCreationForm

User = get_user_model()


# --- AUTHENTICATION ---
def register_view(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('feed:home')
    else:
        form = MyUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('feed:home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('feed:home')


# --- PROFILE & EDITING ---
def profile_view(request, username):
    """Displays the user's profile and their specific uploaded videos."""
    profile_user = get_object_or_404(User, username=username)
    # This variable 'user_videos' must match the loop in your profile.html
    user_videos = Video.objects.filter(user=profile_user).order_by('-created_at')

    # Calculate total likes across all user's videos
    total_likes = sum(v.likes.count() for v in user_videos)

    context = {
        'profile_user': profile_user,
        'user_videos': user_videos,
        'total_likes': total_likes,
        'is_following': profile_user.followers.filter(
            id=request.user.id).exists() if request.user.is_authenticated else False,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """Handles updating profile picture and bio in one step."""
    if request.method == 'POST':
        user = request.user
        user.bio = request.POST.get('bio', user.bio)

        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('users:profile', username=user.username)

    return render(request, 'users/edit_profile.html')


# --- SEARCH ---
def search_users(request):
    query = request.GET.get('q', '')
    results = User.objects.filter(Q(username__icontains=query)).exclude(id=request.user.id) if query else []
    return render(request, 'users/search.html', {'results': results, 'query': query})