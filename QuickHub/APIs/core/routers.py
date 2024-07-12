from rest_framework import routers


class DefaultRouter(routers.DefaultRouter):
    """
    Расширение базового 'DefaultRouter' для того, чтобы роутеры можно было
    настраивать в файле QuickHub.urls так:
    ```
    >> from APIs.core.routers import DefaultRouter
    >> from app1.team_api.urls import router as app1_router
    >> from app2.team_api.urls import router as app2_router

    >> router = DefaultRouter()
    >> router.extend(app1_router)
    >> router.extend(app2_router)
    ```
    """

    def extend(self, router):
        self.registry.extend(router.registry)
