"""
ASGI config for QuickHub project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QuickHub.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
        "http": django_asgi_app,
        # 'websocket': AuthMiddlewareStack(URLRouter(team.routing.websocket_urlpatterns)),
    }
)
