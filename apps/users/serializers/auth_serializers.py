from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only= True)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    #Valida que si la contraseña no es una facil [Naira(moneda_local)]
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este eamil ya esta registrado <Me gusta Lizzy UwU>")
        return value

    def create(self, validated_data):
        email = validated_data["email"].lower().strip()

        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),     
        )
        
        user.phone_number = validated_data.get("phone_number", "")
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only= True)
    
    def validate(self, attrs):
        email = attrs["email"].lower().strip()
        password = attrs["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas.")
        
        if user.is_deleted:
            raise serializers.ValidationError("Usuario Elimnado.")
        
        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Credenciales invalidas. ")
        
        attrs["users"] = user
        return attrs
