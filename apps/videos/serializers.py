from rest_framework import serializers
from .models import Video

class VideoFeedSerializer(serializers.ModelSerializer):
    creator_name = serializers.ReadOnlyField(source='creator.username')
    avatar = serializers.ReadOnlyField(source='creator.avatar.url')
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'video_file', 'description', 'creator_name', 'avatar', 'views', 'like_count']

    def get_like_count(self, obj):
        return obj.likes.count() # Assumes you have a 'likes' related name in Interactions