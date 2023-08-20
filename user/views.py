from django.shortcuts import render
from rest_framework.parsers import JSONParser
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
import random
from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .utils import *
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, filters, viewsets
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView,
    GenericAPIView,
    RetrieveUpdateAPIView,
)
from django.middleware import csrf
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from user.authentication_backends import EmailOrPhoneNumberBackend
from .models import *
from .permissions import IsUserAddressOwner, IsUserProfileOwner
from .serializers import *
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from rest_framework.response import Response


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def get_auth_token(request):
    # Retrieve the user from the request or any other authentication mechanism
    user = request.user

    # Create a token for the user (e.g., during registration or login)
    token, _ = Token.objects.get_or_create(user=user)

    # Retrieve the token value
    token_value = token.key

    return Response({'token': token_value})


def get_csrf_token(request):
    token = csrf.get_token(request)
    return JsonResponse({'csrfToken': token})


# @api_view(['POST'])
# @csrf_exempt
# @permission_classes([AllowAny])
# def create_user(request):
#     if request.method == 'POST':
#         data = request.data
#         phone_number = data.get('phone_number', None)
#         serializer = UserRegistrationSerializer(
#             data=data, context={'request': request, 'phone_number': phone_number})

#         if serializer.is_valid():
#             try:
#                 user = serializer.save()
#                 token = Token.objects.create(user=user)
#                 token_key = token.key
#                 response_data = serializer.data
#                 response_data['token'] = token_key
#                 # response_data['phone_number'] = str(phone_number)  # Convert to string
#                 response_data['phone_number'] = phone_number

#                 # Send SMS verification

#                 return Response(response_data, status=status.HTTP_201_CREATED)
#             except IntegrityError:
#                 return Response({'error': 'Account details already exist.'}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def create_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                user = serializer.save()
                token = Token.objects.create(user=user)
                token_key = token.key
                response_data = serializer.data
                response_data['token'] = token_key
                return Response(response_data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'Account details already exist.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Register(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            # Registration code...
            try:
                user = serializer.save()
                token = Token.objects.create(user=user)
                token_key = token.key
                response_data = serializer.data
                response_data['token'] = token_key
                user.password = make_password(serializer.data['password'])
                user.save()
                
                return Response(response_data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'Account details already exist.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return the validation errors in the response
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# @action(detail=True, methods=["PATCH"])
# def verify_otp(self, request, pk=None):
#     instance = self.get_object()

#     if (
#         not instance.is_active
#         and instance.otp == request.data.get("otp")
#         and instance.otp_expiry
#         and timezone.now() < instance.otp_expiry
#     ):
#         instance.is_active = True
#         instance.otp_expiry = None
#         instance.max_otp_try = settings.MAX_OTP_TRY
#         instance.otp_max_out = None
#         instance.save()
#         send_otp(instance.mobile, otp)
#         return Response(
#             "Successfully verified the user.", status=status.HTTP_200_OK
#         )
#     return Reponse(
#         "User active or Please enter the correct otp.", status=status.HTTP_200_OK
#     )


# @action(detail=True, methods=["PATCH"])
# def regenerate_otp(self, request, pk=None):
#     instance = self.get_object()

#     if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_max_out:
#         return Response(
#             "Max OTP try reached, try after an hour.",
#             status=status.HTTP_400_BAD_REQUEST
#         )
#         otp = random.randInt(1000, 9000)
#         otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
#         max_otp_try = int(instance.max_otp_try) - 1

#         instance.otp = otp
#         instance.otp_expiry = otp_expiry
#         instance.max_otp_try = max_otp_try

#         if max_otp_try == 0:
#             instance.otp_max_out = timezone.now() + datetime.timedelta(hour=1)
#         elif max_otp_try == 1:
#             instance.max_otp_try = settings.MAX_OTP_TRY
#         else:
#             instance.otp_max_out = None
#             instance.max_otp_try = max_otp_try
#         instance.save()

#         send_otp(instance.mobile, otp)

#         return Response("Successfully re-generated the new OTP", status=status.HTTP_200_OK)


class CustomIntegrityError(IntegrityError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


@csrf_exempt
def check_login(request, email):
    try:
        user = User.objects.filter(email=email)
    except:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def get_user(request, id):
    try:
        user = User.objects.get(pk=id)
    except:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')

        if email_or_phone is None:
            return Response({'error': 'Email or phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        authenticated_user = authenticate(request, email_or_phone=email_or_phone, password=password)

        if authenticated_user is not None:
            token, created = Token.objects.get_or_create(user=authenticated_user)
            return Response({'success': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email/phone number or password'}, status=status.HTTP_401_UNAUTHORIZED)



class UserLoginAPIView(APIView):
    """
    Authenticate existing users using phone number or email and password.
    """
    serializer_class = UserLoginSerializer


class ProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsUserProfileOwner,)

    def get_object(self):
        return self.request.user.profile


class AddFrequentUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')  # Assuming the client sends the user_id of the user to add as frequent user
            user = User.objects.get(id=user_id)
            request.user.frequent_users.add(user)
            return Response({'message': 'User added as frequent user'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddFavoriteUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')  # Assuming the client sends the user_id of the user to add as favorite user
            user = User.objects.get(id=user_id)
            request.user.favorite_users.add(user)
            return Response({'message': 'User added as favorite user'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FrequentUsersView(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch frequent users based on the current user's frequent_users relationship
        frequent_users = request.user.frequent_users.all()

        serializer = UserSerializer(frequent_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAPIView(RetrieveAPIView):
    """
    Get user details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["PATCH"])
    def verify_otp(self, request, pk=None):
        instance = self.get_object()

        if (
            not instance.is_active
            and instance.otp == request.data.get("otp")
            and instance.otp_expiry
            and timezone.now() < instance.otp_expiry
        ):
            instance.is_active = True
            instance.otp_expiry = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.otp_max_out = None
            instance.save()
            send_otp(instance.mobile, otp)
            return Response(
                "Successfully verified the user.", status=status.HTTP_200_OK
            )
        return Reponse(
            "User active or Please enter the correct otp.", status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["PATCH"])
    def regenerate_otp(self, request, pk=None):
        instance = self.get_object()

        if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_max_out:
            return Response(
                "Max OTP try reached, try after an hour.",
                status=status.HTTP_400_BAD_REQUEST
            )
            otp = random.randInt(1000, 9000)
            otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
            max_otp_try = int(instance.max_otp_try) - 1

            instance.otp = otp
            instance.otp_expiry = otp_expiry
            instance.max_otp_try = max_otp_try

            if max_otp_try == 0:
                instance.otp_max_out = timezone.now() + datetime.timedelta(hour=1)
            elif max_otp_try == 1:
                instance.max_otp_try = settings.MAX_OTP_TRY
            else:
                instance.otp_max_out = None
                instance.max_otp_try = max_otp_try
            instance.save()

            send_otp(instance.mobile, otp)

            return Response("Successfully re-generated the new OTP", status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



class AddressViewSet(ReadOnlyModelViewSet):
    """
    List and Retrieve user addresses
    """
    queryset = Address.objects.all()
    serializer_class = AddressReadOnlySerializer
    permission_classes = (IsUserAddressOwner,)

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(user=user)



class ProfileCreateView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
