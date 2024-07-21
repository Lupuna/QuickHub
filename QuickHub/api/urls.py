from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views


router = DefaultRouter()
router.register(r'v1/(?P<company>[^/]+)/(?P<datetime_start>\d{4}-\d{2}-\d{2}T\d{2}:\d{2})/(?P<datetime_end>\d{4}-\d{2}-\d{2}T\d{2}:\d{2})',
                views.CompanyEventAPIViewSet, basename='api_company_event')


urlpatterns = [
    path('', include(router.urls))
]

