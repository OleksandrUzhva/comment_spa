from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, CaptchaAPIView

router = DefaultRouter()
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("captcha/", CaptchaAPIView.as_view(), name="api-captcha"),
]

urlpatterns += router.urls