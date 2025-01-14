from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NewsSearchViewSet

router = DefaultRouter()
router.register(r"search", NewsSearchViewSet, basename="news-search")

urlpatterns = [
    path("", include(router.urls)),
]
