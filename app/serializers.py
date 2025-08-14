from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email") or "",
            password=validated_data["password"],
        )


class ParagraphIngestSerializer(serializers.Serializer):
    content = serializers.CharField()

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        # Optional: size guard
        if len(value) > 200_000:
            raise serializers.ValidationError("Content too large.")
        return value


class SearchQuerySerializer(serializers.Serializer):
    word = serializers.CharField()
    limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=10)
