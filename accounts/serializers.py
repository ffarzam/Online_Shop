from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser
from .utils import phoneNumberRegex


class UserRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True, validators=[phoneNumberRegex])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password', 'password2')

    def create(self, validated_data):
        del validated_data['password2']
        return CustomUser.objects.create_user(**validated_data)

    def validate_username(self, value):
        if len(value) < 6 or len(value) > 15:
            raise ValidationError('Username must be between 6 and 15 characters long')
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("username has already been taken")

        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        if data['email'] == data['username']:
            raise serializers.ValidationError("Email and username can't be same")
        if data['password'] == data['username']:
            raise serializers.ValidationError("Password and username can't be same")
        if data['phone'] == data['username']:
            raise serializers.ValidationError("Password and username can't be same")

        return data


class UserLoginSerializer(serializers.Serializer):
    user_identifier = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = '__all__' #???
        exclude = ["password", "groups", "user_permissions"]  # ???


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")

        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError("Email has already been taken")
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(id=user.id).filter(username=value).exists():
            raise serializers.ValidationError("Username has already been taken")
        return value

    def validate_phone(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(id=user.id).filter(username=value).exists():
            raise serializers.ValidationError("Username has already been taken")
        return value

    def update(self, instance, validated_data):

        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.email = validated_data['phone']
        instance.email = validated_data['first_name']
        instance.email = validated_data['last_name']

        instance.save()

        return instance


