import os
from django.core.wsgi import get_wsgi_application

# CRITICAL: This must point to 'config.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()