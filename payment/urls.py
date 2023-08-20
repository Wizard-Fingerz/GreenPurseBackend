from django.urls import path

from .views import register, login_user, logout_user, dashboard, create_wallet, webhook
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CheckoutAPIView, PaymentViewSet, StripeCheckoutSessionCreateAPIView, StripeWebhookAPIView


app_name = 'payment'

router = DefaultRouter()
router.register(r'', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stripe/create-checkout-session/<int:order_id>/',
         StripeCheckoutSessionCreateAPIView.as_view(), name='checkout_session'),
    path('stripe/webhook/', StripeWebhookAPIView.as_view(), name='stripe_webhook'),
    path('checkout/<int:pk>/', CheckoutAPIView.as_view(), name='checkout'),

]
# urlpatterns = [
#     path('dashboard', dashboard, name="dashboard"),
#     path('register/', register, name="register"),
#     path('login/', login_user, name="login"),
#     path('logout/', logout_user, name="logout"),
#     path('verify/', create_wallet, name='verify'),
#     path(
#         "webhooks/wallets_africa/aDshFhJjmIalgxCmXSj/",
#          webhook,
#          name = "webhook"
#     ),
# ]
