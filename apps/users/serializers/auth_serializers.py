from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Importación esencial para el nuevo Login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # Definimos los campos con mensajes de error claros (UX para el frontend)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="Este email ya está registrado."
            )
        ]
    )

    dni = serializers.CharField(
        validators=[
            RegexValidator(regex=r"^\d{8}$", message="El DNI debe tener 8 dígitos."),
            UniqueValidator(
                queryset=User.objects.all(), message="Este DNI ya está registrado."
            ),
        ]
    )

    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[
            RegexValidator(regex=r"^\d{9}$", message="Debe ser un número de 9 dígitos.")
        ],
    )

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "dni",
            "phone_number",
            "birth_date",
            "password",
            "password2",
        )

    def validate(self, attrs):
        # 1. Validación de contraseñas
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden."}
            )

        # 2. Normalización profesional
        attrs["email"] = attrs["email"].lower().strip()
        attrs["username"] = attrs["email"]
        return attrs

    def create(self, validated_data):
        # Usamos el manager de Django para el hashing automático de la password
        return User.objects.create_user(**validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Sustituye a tu LoginSerializer manual.
    SimpleJWT se encarga de validar email/password automáticamente.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadimos Custom Claims (Datos extra dentro del JWT)
        # Esto permite que el frontend lea estos datos sin pegarle a la DB
        token["first_name"] = user.first_name
        token["email"] = user.email
        token["role"] = getattr(user, "role", "user")

        return token
