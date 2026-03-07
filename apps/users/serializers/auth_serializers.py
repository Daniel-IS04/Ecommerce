from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password 
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(required=True, allow_blank=False,error_messages={
        "blank": "Rellena el nombre ctmr, no pude estar vacio",
        "required": "Rellena mierda",
    })  
    last_name = serializers.CharField(required=True, allow_blank=False,error_messages={
        "blank": "Rellena el nombre ctmr, no pude estar vacio",
        "required": "Rellena mierda",
    })

    password = serializers.CharField(write_only= True)
    password2 = serializers.CharField(write_only= True)
    class Meta:
        model = User
        # es lo que se nos envio de la request
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
    def validate_email(self, value):
        email = value.lower().strip()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este email ya esta registrado")
        return email
    
    def validate_dni(self, value: str):
        dni = value
        if(len(dni)== 8 and dni.isdigit()):
            if( not User.objects.filter(dni=dni).exists()):
                return dni    
            raise serializers.ValidationError("Este DNI ya esta registrado")
        raise serializers.ValidationError("Este valor no cumple con los requisitos")

    def validate_password(self, value):
        validate_password(value)
        return value
    
    def validate_phone_number(self, value):
        if value in (None, ""):
            return value
        
        if not (value.isdigit() and len(value)) == 9:
            raise serializers.ValidationError("No cumple con las condiciones de un numero peruano")
        return value

    def create(self, validated_data):
        # 1) saca password2
        validated_data.pop("password2")

        # 2) saca password real
        raw_password = validated_data.pop("password")

        # 3) normaliza email
        email = validated_data["email"].lower().strip()
        validated_data["email"] = email

        # 4) si tu regla es username=email:
        validated_data["username"] = email

        # 5) crea usuario sin password plano
        user = User(**validated_data)
        user.set_password(raw_password)
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
        
        
        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Credenciales invalidas. ")
        
        attrs["user"] = user
        return attrs
