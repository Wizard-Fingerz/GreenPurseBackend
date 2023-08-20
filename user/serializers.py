from rest_framework import serializers
from .models import *
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework.validators import UniqueValidator
# from dj_rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from django_countries.serializers import CountryFieldMixin
import random
from datetime import datetime, timedelta
from .exceptions import (
    AccountNotRegisteredException,
    InvalidCredentialsException,
    AccountDisabledException,
)
from .utils import *


from rest_framework import serializers

class BigIntegerField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return int(data)
        except (TypeError, ValueError):
            raise serializers.ValidationError('Invalid integer value')



# class PhoneNumberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PhoneNumber
#         fields = ['number']


# class PhoneNumberSerializer(serializers.ModelSerializer):
#     phone_number = serializers.IntegerField()

#     class Meta:
#         model = PhoneNumber
#         fields = ('phone_number',)

#     def validate_phone_number(self, value):
#         # Perform validation checks on the phone number
#         # For example, check if the phone number is already registered or verified
#         # You can customize this validation logic based on your requirements
#         try:
#             queryset = User.objects.get(phone__phone_number=value)
#             if queryset.phone.is_verified:
#                 raise serializers.ValidationError(
#                     'Phone number is already verified')
#         except User.DoesNotExist:
#             raise serializers.ValidationError('Invalid phone number')

#         return value


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()  # Or use serializers.RegexField(regex=r'^\+?1?\d{9,15}$') for phone number validation
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # phone_number = serializers.IntegerField(required = True, write_only = True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'password']

    def validate(self, validated_data):
        email = validated_data.get('email', None)
        phone_number = validated_data.get('phone_number', None)

        if not (email or phone_number):
            raise serializers.ValidationError(
                _("Enter an email or a phone number."))

        return validated_data

    def get_cleaned_data_extra(self):
        return {
            'phone_number': self.validated_data.get('phone_number', ''),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }

    def create_extra(self, user, validated_data):
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.save()

        phone_number = validated_data.get("phone_number")

    
        user.phone_number = phone_number
        user.save()

    def custom_signup(self, request, user):
        self.create_extra(user, self.get_cleaned_data_extra())

    def to_internal_value(self, data):
        """
        Perform the validation and conversion of input data.
        """
        if 'phone_number' in data:
            # Normalize the phone number input
            phone_number = self.fields['phone_number'].to_internal_value(
                data['phone_number'])
            data['phone_number'] = phone_number

        return super().to_internal_value(data)

    def create(self, validated_data):
        # otp = random.randint(1000, 9999)
        # otp_expiry = datetime.now() + timedelta(minutes= 10)
        phone_number = self.context.get('phone_number')

        # Create and save the User instance
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            phone_number=validated_data.get('phone_number'),
            # otp = otp,
            # otp_expiry = otp_expiry,
            # max_otp_try = settings.MAX_OTP_TRY,
        )

        # Save any additional data
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.save()
        
        # TODO: call send_otp function
        # send_otp(phone_number, otp)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer to login users with email or phone number.
    """
    phone_number = PhoneNumberField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def _validate_phone_email(self, phone_number, email, password):
        user = None

        if email and password:
            user = authenticate(username=email, password=password)
        elif str(phone_number) and password:
            user = authenticate(username=str(phone_number), password=password)
        else:
            raise serializers.ValidationError(
                _("Enter a phone number or an email and password."))

        return user

    def validate(self, validated_data):
        phone_number = validated_data.get('phone_number')
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = None

        user = self._validate_phone_email(phone_number, email, password)

        if not user:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise AccountDisabledException()

        if email:
            email_address = user.emailaddress_set.filter(
                email=user.email, verified=True).exists()
            if not email_address:
                raise serializers.ValidationError(_('E-mail is not verified.'))

        else:
            if not user.phone.is_verified:
                raise serializers.ValidationError(
                    _('Phone number is not verified.'))

        validated_data['user'] = user
        return validated_data


# class VerifyPhoneNumberSerialzier(serializers.Serializer):
#     """
#     Serializer class to verify OTP.
#     """
#     phone_number = serializers.IntegerField()
#     # phone_number = PhoneNumberField()
#     otp = serializers.CharField(max_length=settings.TOKEN_LENGTH)

#     def validate_phone_number(self, value):
#         queryset = User.objects.filter(phone__phone_number=value)
#         if not queryset.exists():
#             raise AccountNotRegisteredException()
#         return value

#     def validate(self, validated_data):
#         phone_number = str(validated_data.get('phone_number'))
#         otp = validated_data.get('otp')

#         queryset = PhoneNumber.objects.get(phone_number=phone_number)

#         queryset.check_verification(security_code=otp)

#         return validated_data


# class ProfileSerializer(serializers.ModelSerializer):
#     """
#     Serializer class to serialize the user Profile model
#     """
#     class Meta:
#         model = Profile
#         fields = ('avatar', 'bio', 'created_at', 'updated_at',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio',)
        # read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class AddressReadOnlySerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer class to seralize Address model
    """
    user = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to seralize User model
    """
    profile = ProfileSerializer(read_only=True)
    phone_number = PhoneNumberField(source='phone', read_only=True)
    addresses = AddressReadOnlySerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name',
                  'last_name', 'is_active', 'profile', 'addresses',)


class ShippingAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer class to seralize address of type shipping

    For shipping address, automatically set address type to shipping
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('address_type', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['address_type'] = 'S'

        return representation


class BillingAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer class to seralize address of type billing

    For billing address, automatically set address type to billing
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('address_type', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['address_type'] = 'B'

        return representation
