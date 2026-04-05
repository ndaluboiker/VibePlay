from django.db import models
from apps.users.models import User
from apps.videos.models import Video


class Report(models.Model):
    REPORT_REASONS = [
        ('spam', 'Spam/Scam'),
        ('hate', 'Hate Speech'),
        ('violence', 'Graphic Content'),
        ('copyright', 'Copyright Infringement'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_filed')
    target_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='reports_received')
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report: {self.reason} against {self.target_user or self.target_video}"