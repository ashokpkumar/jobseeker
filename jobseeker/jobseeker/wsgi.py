"""
WSGI config for jobseeker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/home/nikhith/jobseeker_env/env/lib/python3.12/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobseeker.settings")

application = get_wsgi_application()
