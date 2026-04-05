from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from apps.videos.models import Video
from .models import Comment, Like, Notification
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def ajax_like(request, video_id):
    """Handles Liking/Unliking via AJAX"""
    video = get_object_or_404(Video, id=video_id)
    like_qs = Like.objects.filter(user=request.user, video=video)
    if like_qs.exists():
        like_qs.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, video=video)
        liked = True
        if request.user != video.user:
            Notification.objects.create(recipient=video.user, sender=request.user, notification_type='like',
                                        video=video)
    return JsonResponse({'liked': liked, 'likes_count': video.likes.count()})


@login_required
def ajax_follow(request, user_id):
    """Handles TikTok-style Following/Unfollowing via AJAX"""
    target_user = get_object_or_404(User, id=user_id)
    if request.user == target_user:
        return JsonResponse({'followed': False, 'error': 'Self-follow not allowed'})

    # Check if current user is already in target_user's followers
    if target_user.followers.filter(id=request.user.id).exists():
        target_user.followers.remove(request.user)
        followed = False
    else:
        target_user.followers.add(request.user)
        followed = True
        Notification.objects.create(recipient=target_user, sender=request.user, notification_type='follow')

    return JsonResponse({
        'followed': followed,
        'follower_count': target_user.follower_count
    })


def get_comments(request, video_id):
    """Returns all comments for a specific video as JSON"""
    video = get_object_or_404(Video, id=video_id)
    comments = Comment.objects.filter(video=video).order_by('-created_at')
    comments_list = []
    for c in comments:
        pic = c.user.profile_pic.url if c.user.profile_pic else ""
        comments_list.append({
            'username': c.user.username,
            'text': c.text,
            'profile_pic': pic,
            'created_at': c.created_at.strftime("%b %d, %Y")
        })
    return JsonResponse({'comments': comments_list})


@login_required
def ajax_post_comment(request, video_id):
    """Posts a comment via AJAX"""
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, video=video, text=text)
            if request.user != video.user:
                Notification.objects.create(recipient=video.user, sender=request.user, notification_type='comment',
                                            video=video)
            return JsonResponse({'status': 'success', 'username': request.user.username, 'text': text})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def check_notifications(request):
    """API for the red badge on the Inbox icon"""
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})


@login_required
def inbox_view(request):
    """Displays the user's notification center"""
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'interactions/inbox.html', {'notifications': notifications})


def search_vibes(request):
    """Handles global search for videos and users"""
    query = request.GET.get('q', '').strip()
    if query:
        videos = Video.objects.filter(Q(description__icontains=query) | Q(user__username__icontains=query)).distinct()
    else:
        videos = []
    return render(request, 'feed/search_results.html', {'videos': videos, 'query': query})