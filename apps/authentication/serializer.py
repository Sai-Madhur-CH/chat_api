from rest_framework import serializers
from django.core.validators import ValidationError
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
import json
from django.forms.models import model_to_dict


def check_min_lenght(value):
    if len(value) < 8:
        raise ValidationError(
            _('Password must be 8 characters.'), params={'value': value})


def check_for_digit(value):
    if not any(char.isdigit() for char in value):
        raise ValidationError(
            _('Password must contain at least 1 digit.'), params={'value': value})


def check_for_letter(value):
    if not any(char.isalpha() for char in value):
        raise ValidationError(
            _('Password must contain at least 1 letter.'), params={'value': value})


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(
        validators=[check_min_lenght, check_for_digit, check_for_letter])
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        print('User created Successfully.')
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True}
        }

    @receiver(post_save, sender=User)
    def auth(self, validated_data, **kwargs):
        user = User.objects.get(email=validated_data.get('email'))
        if user and user.check_password(validated_data.get('password')):
            user_token = Token.objects.filter(user=user)
            if user_token:
                key = user_token[0].generate_key()
                user_token.update(key=key)
                print('TOKEN UPDATED', key)
            else:
                token = Token.objects.create(user=user)
                key = token.key
                print('TOKEN CREATED', token.key)
            return self.success_json_response(key, user)
        else:
            return self.failure_json_response()

    def success_json_response(self, token, user):
        obj = model_to_dict(
            user, fields=['id', 'username', 'email', 'first_name', 'last_name'])
        obj['token'] = token
        obj['status'] = 'success'
        return obj

    def failure_json_response(self):
        return {'status': 'UnAuthorized User'}
