from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
        ]