"""
WSGI config for market_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from market_backend.env_dir.base import set_environment

set_environment()
application = get_wsgi_application()
