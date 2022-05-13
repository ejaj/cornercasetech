from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from user.models import Employees

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A Serializer class for user
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = ('id', 'name', 'email', 'password', 'password2')
        extra_kwargs = {
            'name': {'required': True}
        }

    def validate(self, attrs):
        """
        Check passwords are match
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        user = UserModel.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            is_active=True
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class EmployeeSerializer(serializers.ModelSerializer):
    """
    A Serializer class for employee
    """
    employee_id = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Employees.objects.all())]
    )

    class Meta:
        model = Employees
        fields = ['id', 'name', 'employee_id', 'department', 'status']
        extra_kwargs = {
            'name': {'required': True},
            'department': {'required': True},
        }
