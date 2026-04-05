import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Video
from apps.interactions.models import Comment, Notification, Like

# 1. THE MAIN FEED (Initial Load)
def feed_view(request):
    """Initial page load with 3 random videos to start the TikTok loop."""
    all_videos = list(Video.objects.all())
    random.shuffle(all_videos)
    # Take the first 3 to start the loop
    initial_videos = all_videos[:3]
    return render(request, 'feed/main_feed.html', {'videos': initial_videos})


# 2. THE SHUFFLE ENGINE (Infinite Scroll API)
def get_shuffled_chunk(request):
    """
    API called by JavaScript for Infinite Scroll.
    Returns random videos excluding those already seen.
    """
    seen_ids = request.GET.getlist('seen_ids[]')

    # Get videos not in the seen list
    available_vids = list(Video.objects.exclude(id__in=seen_ids))

    # If user has seen everything, reset the pool (Infinite Loop)
    if len(available_vids) < 3:
        available_vids = list(Video.objects.all())

    random.shuffle(available_vids)
    selection = available_vids[:3]

    data = []
    for v in selection:
        # Check if the current user is already following the uploader
        is_following = False
        if request.user.is_authenticated:
            is_following = request.user.following.filter(id=v.user.id).exists()

        data.append({
            'id': str(v.id),
            'video_url': v.file.url,
            'username': v.user.username,
            'user_id': str(v.user.id),
            'profile_pic': v.user.profile_pic.url if v.user.profile_pic else None,
            'description': v.description,
            'is_following': is_following,
            'likes_count': v.likes.count(),
            'comments_count': v.comments.count(),
        })

    return JsonResponse({'videos': data})


# 3. UPLOAD (Direct Device Browse & Camera)
@login_required
def upload_video(request):
    """Handles direct file browse from device or camera recording."""
    if request.method == 'POST':
        video_file = request.FILES.get('file')
        description = request.POST.get('description', f"Vibe from {request.user.username}")

        if video_file:
            new_video = Video.objects.create(
                user=request.user,
                file=video_file,
                description=description
            )
            # After upload, send user to their profile to see the new video
            return redirect('users:profile', username=request.user.username)

    # Fallback for manual upload page if needed
    return render(request, 'videos/upload.html')


# 4. TIKTOK-STYLE COMMENTING (AJAX)
@login_required
def add_comment_ajax(request, video_id):
    """Allows posting comments without refreshing the video."""
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        text = request.POST.get('text')

        if text:
            comment = Comment.objects.create(
                video=video,
                user=request.user,
                text=text
            )

            # Notify the video owner
            if request.user != video.user:
                Notification.objects.create(
                    recipient=video.user,
                    sender=request.user,
                    notification_type='comment',
                    video=video
                )

            return JsonResponse({
                'status': 'success',
                'username': request.user.username,
                'text': text,
                'created_at': 'Just now'
            })
    return JsonResponse({'status': 'error'}, status=400)


# 5. VIDEO DETAIL (For Profile Grid Clicks)
def video_detail(request, video_id):
    """View a single video (useful for clicks from the profile grid)."""
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'videos/video_detail.html', {'video': video})