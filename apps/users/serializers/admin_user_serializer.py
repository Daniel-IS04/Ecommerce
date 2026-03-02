from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

#primero traemos mi modulo creado personalizado gaaa
User = get_user_model()

#un serializador es poder transformar datos (json, txt) a python
class AdminUserSerizalizer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Por favor no puedes crear un user sin nombre pe",
            "required": "Rellenarlo por favor"
        }
    )
    last_name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Por favor no puedes crear un user sin apellido(Quispe) pe",
            "required": "Rellenarlo por favor"
        }
    )
    email = serializers.EmailField()

    # para actulizzar el password 
    password = serializers.CharField(
        write_only=True,
        required=False,  # <- para que en update no sea obligatorio
        help_text="Password solo para la creacion o cambio",
        trim_whitespace=False
    )

    phone_number = serializers.CharField(required=False, allow_blank=True)

    #para actualizar el is_active
    is_active = serializers.BooleanField(
        required=False,
    )

    class Meta:
        #es decirle a nuestro serializador
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "is_active",
            "password",
        ]
        read_only_fields = ["id"]  # <- corregido

    # el crate es un metodo heredado no lo hicimos nosotros
    #el validate_data 
    def validate_password(self, value):
        # en update self.instance existe, en create self.instance es None
        if value is None or value == "":
            return value
        validate_password(value, self.instance)
        return value

    def validate_phone_number(self, value):
        if value and (not value.isdigit()):
            raise serializers.ValidationError("Todos tienen que ser numeros")
        return value

    def create(self, validated_data):
        email = validated_data["email"].lower().strip()
        password = validated_data.pop("password", None)

        # si lo vas a usar para crear, entonces acá sí exigimos password
        if not password:
            raise serializers.ValidationError({"password": "La contraseña es obligatoria al crear."})

        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=email,
            email=email,
            password=password
        )

        user.phone_number = validated_data.get("phone_number", "")
        user.save()
        return user

    def update(self, instance, validated_data):
        # noralizar tanto password despues del validate
        password = validated_data.pop("password", None)
        is_active = validated_data.pop("is_active", None)

        if password:
            validate_password(password, instance)
            instance.set_password(password)

        if is_active is not None:
            instance.is_active = is_active

        instance.save()
        return instance
