from rest_framework import viewsets, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment
from .serializers import CommentSerializer
from .captcha_utils import generate_captcha, validate_captcha


class CommentsPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = CommentSerializer
    pagination_class = CommentsPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["user_name", "email", "created_at"]
    ordering = ["-created_at"]  

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        captcha_key = data.pop("captcha_hashkey", None) or data.pop("captcha_key", None)
        captcha_value = data.pop("captcha_value", None)

        if not validate_captcha(captcha_key, captcha_value):
            return Response(
                {"detail": "Invalid CAPTCHA"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CaptchaAPIView(APIView):
    def get(self, request, format=None):
        data = generate_captcha()
        return Response(data)