from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import *

app_name = 'users'

router = DefaultRouter()
router.register(r'', UserViewSet, basename = 'user')

urlpatterns = [
    path('register/', create_user, name='user_register'),
    path('register2/', Register.as_view(), name='user_register'),
    # path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('login/', Login.as_view(), name = 'login'),
    # path('send-sms/', SendOrResendSMSAPIView.as_view(), name='send_resend_sms'),
    # path('verify-phone/', VerifyPhoneNumberAPIView.as_view(), name='verify_phone_number'),
    path('', UserAPIView.as_view(), name='user_detail'),
    # path('profile/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    # path('profile/', ProfileAPIView.as_view(), name='profile_detail'),
    path('profile/address/', include(router.urls)),
    path('add_frequent_user/', AddFrequentUserView.as_view(), name='add-frequent-user'),
    path('get_frequent_users/', FrequentUsersView.as_view(), name='get-frequent-user'),
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),
    path('api-auth-token', obtain_auth_token, name='api_token'),
    # path('accounts/', include('allauth.urls')),
    # path('dj_rest_auth/', include('dj_rest_auth.urls')),
    path('profile/', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/<int:pk>/', ProfileRetrieveUpdateView.as_view(), name='profile-retrieve-update'),
]

urlpatterns += router.urls
