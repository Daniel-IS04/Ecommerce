# auth_serializer.py (o donde tengas RegisterSerializer)

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer de registro:
    - Usa ModelSerializer porque SÍ estamos creando un User (modelo real).
    - Añade 'password2' (confirmación) que NO existe en el modelo.
    """

    # ✅ password: solo entrada, nunca debe devolverse en response
    password = serializers.CharField(write_only=True)

    # ✅ password2: solo sirve para comparar, tampoco se devuelve
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # ✅ SOLO campos permitidos en registro (NO role, NO is_staff, etc.)
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

    # ---------- VALIDACIONES POR CAMPO (validate_<campo>) ----------

    def validate_email(self, value: str) -> str:
        """
        Normaliza el email:
        - lower() para evitar duplicados por mayúsculas
        - strip() para eliminar espacios
        El unique del modelo + ModelSerializer ya detecta duplicados.
        """
        return value.lower().strip()

    def validate_password(self, value: str) -> str:
        """
        Valida fuerza de contraseña usando los validadores de Django.
        Esto usa lo que tengas en settings.AUTH_PASSWORD_VALIDATORS.
        """
        validate_password(value)
        return value

    def validate_phone_number(self, value: str) -> str:
        """
        Si mandan phone_number:
        - solo números
        - largo 9 (Perú típico)
        Si viene vacío o None, lo dejamos pasar.
        """
        if value in (None, ""):
            return value

        if not value.isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo números.")
        if len(value) != 9:
            raise serializers.ValidationError("El teléfono debe tener 9 dígitos.")
        return value

    def validate_dni(self, value: str) -> str:
        """
        Si mandan DNI:
        - solo números
        - largo 8 (DNI Perú típico)
        Si viene vacío o None, lo dejamos pasar.
        """
        if value in (None, ""):
            return value

        if not value.isdigit():
            raise serializers.ValidationError("El DNI debe contener solo números.")
        if len(value) != 8:
            raise serializers.ValidationError("El DNI debe tener 8 dígitos.")
        return value

    # ---------- VALIDACIÓN GLOBAL (validate) ----------

    def validate(self, attrs: dict) -> dict:
        """
        Validación que depende de varios campos:
        - password y password2 deben coincidir
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden."}
            )
        return attrs

    # ---------- CREACIÓN (create) ----------

    def create(self, validated_data: dict) -> User:
        """
        Aquí se crea el usuario.
        Puntos CLAVE:
        - 'password2' no sirve para guardar -> se elimina
        - La password se HASHEA con set_password()
        - Como tu User hereda de AbstractUser, existe 'username'
          y tú dijiste que quieres evitar conflictos: username = email
        """

        # 1) Sacamos campos que no van al modelo
        validated_data.pop("password2")

        # 2) Extraemos password para hashearla manualmente
        raw_password = validated_data.pop("password")

        # 3) Normalizamos email (por si viene raro)
        email = validated_data["email"].lower().strip()

        # 4) Creamos instancia sin password (todavía)
        user = User(**validated_data)

        # 5) Regla de tu proyecto: username = email
        user.username = email
        user.email = email

        # 6) Hashear password correctamente
        user.set_password(raw_password)

        # 7) Guardar en DB
        user.save()
        return user

