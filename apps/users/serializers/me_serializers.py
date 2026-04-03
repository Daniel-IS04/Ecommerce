from django.contrib.auth import get_user_model

# from django.core import validators
from rest_framework import serializers
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    email = serializers.CharField(
        required=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="Este email ya registro."
            )
        ],
    )
    phone_number = serializers.CharField(
        required=False,
        validators=[RegexValidator(regex=r"^\d{9}$", message="Numero de digitos es 9")],
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]
