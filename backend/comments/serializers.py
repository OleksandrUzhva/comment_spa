from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "user_name",
            "email",
            "homepage",
            "text",
            "parent",
            "is_blocked",
            "created_at",
        )

    def validate_user_name(self, value):
        if not value.isalnum():
            raise serializers.ValidationError(
                "User name must contain only Latin letters and digits."
            )
        return value

    def validate_text(self, value):
        import re
        cleaned = re.sub(r"<[^>]*?>", "", value)
        if not cleaned.strip():
            raise serializers.ValidationError("Text cannot be empty after stripping HTML.")
        return cleaned