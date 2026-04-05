import os
from django.conf import settings
from apps.videos.models import Video

class VideoService:
    """
    Logic for Video Management and Discovery.
    """
    @staticmethod
    def get_trending_videos(limit=10):
        """
        Returns the top videos based on view count.
        """
        return Video.objects.all().order_by('-views')[:limit]

    @staticmethod
    def upload_video_logic(user, video_file, description, thumbnail=None):
        """
        Handles the creation of a video record.
        """
        video = Video.objects.create(
            creator=user,
            video_file=video_file,
            description=description,
            thumbnail=thumbnail
        )
        return video

    @staticmethod
    def delete_video(video_id, user):
        """
        Ensures only the owner can delete their video.
        """
        video = Video.objects.filter(id=video_id, creator=user).first()
        if video:
            # Remove the physical file from storage
            if video.video_file:
                if os.path.isfile(video.video_file.path):
                    os.remove(video.video_file.path)
            video.delete()
            return True
        return False