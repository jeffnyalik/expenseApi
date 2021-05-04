from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from authentication.models import User
from rest_framework.response import Response
from rest_framework import status

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'password2', 'password']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({'UNAUTHORIZED':'YOU ARE NOT ALLOWED'})

        instance.set_password(validated_data['password'])
        instance.save()
        return Response("Success")


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
