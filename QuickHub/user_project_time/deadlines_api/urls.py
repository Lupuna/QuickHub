from rest_framework.routers import DefaultRouter

from user_project_time.deadlines_api import views

app_name = "deadlines_api"

router = DefaultRouter()
router.register(r"deadlines", views.DeadlinesViewSet)
