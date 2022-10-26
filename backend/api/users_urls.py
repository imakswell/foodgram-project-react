from api.views.users_views import ListSubscriptions, Subscribe
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", ListSubscriptions, basename="subscriptions")

urlpatterns = [
    path("users/subscriptions/", include(router.urls)),

    path("users/<int:id>/subscribe/", Subscribe.as_view(), name="subscribe"),
    path(r"", include("djoser.urls")),
    re_path("auth/", include("djoser.urls.authtoken")),
]
