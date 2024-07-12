"""QuickHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from QuickHub import settings

from APIs.core.routers import DefaultRouter
from team.team_api.urls import router as team_router
from user_project.taskboards_api.urls import router as user_project_router
from user_project_time.deadlines_api.urls import router as user_project_time_router


handler403 = 'team.views.error403'

router = DefaultRouter()
router.extend(team_router)
router.extend(user_project_router)
router.extend(user_project_time_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('team-taskboard/', include('user_project.urls', namespace='user_project')),
    path('team-deadlines/', include('user_project_time.urls', namespace='user_project_time')),
    path('team/', include('team.urls', namespace='team')),
    path('account/', include('q_registration.urls', namespace='q_registration')),

    path(r'api/v1/', include(router.urls)),

    path('api_schema/', SpectacularAPIView.as_view(), name='api_schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api_schema'), name='swagger-ui'),

    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/auth/', include('djoser.urls')),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls")), ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
