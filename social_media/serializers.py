from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from social_media.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id", "email", "name", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        member = Member(
            email=validated_data['email'].lower(),
            name=validated_data['name']
        )
        member.set_password(validated_data['password'])
        member.save()
        Token.objects.create(user=member)
        return member

    def validate(self, data):
        email = data['email'].lower()
        if Member.objects.filter(email=email).exists():
            raise ValidationError("member with this email already exists")
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')
        member = self.authenticate(email=email, password=password)
        if member is None:
            raise ValidationError('Invalid email or password')
        token = Token.objects.get(user=member)
        return {"token": str(token)}

    def authenticate(self, email, password):
        try:
            member = Member.objects.get(email=email)
        except Member.DoesNotExist:
            raise ValidationError("Invalid email")
        if member.check_password(password):
            if member.is_active:
                return member
            raise ValidationError("Member not active")
        raise ValidationError("Invalid password")
