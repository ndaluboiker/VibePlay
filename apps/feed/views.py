from django.views.generic import ListView
from apps.videos.models import Video
from django.db.models import Q

class HomeView(ListView):
    model = Video
    template_name = 'feed/home.html'
    context_object_name = 'videos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # Search both description and username
            return Video.objects.filter(
                Q(description__icontains=query) |
                Q(creator__username__icontains=query)
            )
        # Shuffle logic: '?' returns random results for a fresh feed
        return Video.objects.all().order_by('?')