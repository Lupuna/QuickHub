from rest_framework.routers import DefaultRouter

from user_project.taskboards_api.views import CategoryViewSet

app_name = "taskboards_api"

router = DefaultRouter()
router.register(r"taskboard", CategoryViewSet)

