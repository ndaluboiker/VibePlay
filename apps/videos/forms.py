from django import forms
from .models import Video


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        # These are the fields the user fills out
        fields = ['video_file', 'description']

        # Adding some CSS classes so it looks like TikTok
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Write a caption...',
                'style': 'width: 100%; height: 100px; border-radius: 8px; padding: 10px; border: 1px solid #ddd;'
            }),
            'video_file': forms.FileInput(attrs={
                'accept': 'video/*',
                'style': 'margin-top: 10px;'
            }),
        }