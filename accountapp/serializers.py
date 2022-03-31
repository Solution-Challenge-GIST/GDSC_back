from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.db import transaction
from rest_framework import serializers
from accountapp.models import User, ROLE_SELECTION
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.core.exceptions import ValidationError as DjangoValidationError

from juniorapp.serializers import JuniorSerializer
from seniorapp.serializers import SeniorSerializer


class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=ROLE_SELECTION)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'role',
        )
        read_only_fields = ('pk', 'email', 'role',)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = User.objects.create(
            email=self.data.get('email'),
        )
        user.set_password(self.data.get('password'))
        user.role = self.data.get('role')
        adapter = get_adapter()
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

    def validate_password1(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']


class JuniorUserSerializer(UserSerializer):
    junior = JuniorSerializer()

    class Meta:
        model = User
        depth = 1
        fields = ['id', 'email', 'role', 'junior']


class SeniorUserSerializer(UserSerializer):
    senior = SeniorSerializer()

    class Meta:
        model = User
        depth = 1
        fields = ['id', 'email', 'role', 'senior']