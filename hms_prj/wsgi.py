"""
WSGI config for hms_prj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_prj.settings')

application = get_wsgi_application()
from whitenoise import WhiteNoise
from django.conf import settings

application = WhiteNoise(application, root=settings.STATIC_ROOT)  # serve /static/
application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)  # serve /media/
