from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.db.transaction import atomic, non_atomic_requests
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ipaddress import ip_address, ip_network
import json 
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, CustomAuthForm, BVNForm
from .decorators import verified

from .api import WalletsClient
from .models import *

from cryptography.fernet import Fernet
# Create your views here.


wallet = WalletsClient(secret_key="hfucj5jatq8h", public_key="uvjqzm5xl6bw")
fernet = Fernet(settings.ENCRYPTION_KEY)


def register(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'Account succesfully created. You can now login')
            return redirect('accounts:login')
    return render(request, "accounts/register.html", context = {"form":form})

def login_user(request):
    form = CustomAuthForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email = cd['email'], password=cd['password']) 
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next','accounts:dashboard'))
            else:
                messages.error(request, 'Account does not exist')
    return render(request, "accounts/login.html", context = {"form":form})

@login_required
def logout_user(request):
    logout(request)
    return redirect("accounts:login")


@login_required
@verified
def dashboard(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    return render(request, "dashboard.html", context={"wallet":wallet})

@login_required
def create_wallet(request):
    form = BVNForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            bvn = cd["bvn"]
            new_wallet = wallet.create_user_wallet(
                    first_name= user.first_name,
                    last_name= user.last_name,
                    email=user.email,
                    date_of_birth= user.date_of_birth.strftime('%Y-%m-%d'),
                    bvn= str(bvn)
                )
            if new_wallet["response"]["responseCode"] == '200':
                user.verified = True
                user.save()
                Wallet.objects.create(
                    user = user,
                    balance = new_wallet["data"]["availableBalance"],
                    account_name = new_wallet["data"]["accountName"],
                    account_number = new_wallet["data"]["accountNumber"],
                    bank = new_wallet["data"]["bank"],
                    phone_number = new_wallet["data"]["phoneNumber"],
                    password = fernet.encrypt(new_wallet["data"]["password"].encode())
                )
                messages.success(request, "Account verified, wallet successfully created")
                return redirect("accounts:dashboard")
            else:
                messages.error(request, new_wallet["response"]["message"])
           
    return render(request, "accounts/bvn.html", context = {"form":form})

def make_transaction(request):
    if request.method == 'POST':
        try:
            sender = request.POST.get('sender')
            recipient = request.POST.get('recipient')
            amount = request.POST.get('amount')
            
            with transaction.atomic():
                sender_obj = Payment.objects.get(user = sender)
                sender_obj.amount -= int(amount)
                sender_obj.save()
                
                recipient_obj = Payment.objects.get(user = recipient)
                recipient_obj.amount += int(amount)
                recipient_obj.save()
                messages.success(request, 'YOur amount is transfered')
        except Exception as e:
            print(e)
            messages.success(request, 'Something went wrong')
        return redirect('/')
    return render(request, 'home.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect("accounts:login") 


@csrf_exempt
@require_POST
def webhook(request):
    whitelist_ip = "18.158.59.198"
    forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
    client_ip_address = ip_address(forwarded_for)

    if client_ip_address != ip_network(whitelist_ip):
        return HttpResponseForbidden('Permission denied.')

    payload = json.loads(request.body)
    try:
        if payload['EventType'] == "BankTransferPayout":
            pass
        elif payload['EventType'] == "BankTransferFunding":
            pass
        else:
            pass
        return HttpResponse(status=200)

    except:
        if payload['TransactionType'] == "credit":
            pass
        elif payload['TransactionType'] == "debit":
            pass
        else:
            pass
        return HttpResponse(status=200)

# khjkjeklkjhgyftdfghjjiuygtfdfhbnbvgfcdxfcgvb


from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import stripe

from payment.models import Payment
from payment.permissions import (
    DoesOrderHaveAddress,
    IsOrderPendingWhenCheckout,
    IsPaymentByUser,
    IsPaymentForOrderNotCompleted,
    IsPaymentPending
)
from payment.serializers import CheckoutSerializer, PaymentSerializer
from orders.models import Order
from orders.permissions import IsOrderByBuyerOrAdmin
from payment.tasks import send_payment_success_email_task


stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(ModelViewSet):
    """
    CRUD payment for an order
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsPaymentByUser]

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(order__buyer=user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes += [IsPaymentPending]

        return super().get_permissions()


class CheckoutAPIView(RetrieveUpdateAPIView):
    """
    Create, Retrieve, Update billing address, shipping address and payment of an order
    """
    queryset = Order.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [IsOrderByBuyerOrAdmin]

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            self.permission_classes += [IsOrderPendingWhenCheckout]

        return super().get_permissions()


class StripeCheckoutSessionCreateAPIView(APIView):
    """
    Create and return checkout session ID for order payment of type 'Stripe'
    """
    permission_classes = (IsPaymentForOrderNotCompleted,
                          DoesOrderHaveAddress, )

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))

        order_items = []

        for order_item in order.order_items.all():
            product = order_item.product
            quantity = order_item.quantity

            data = {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount_decimal': product.price,
                    'product_data': {
                        'name': product.name,
                        'description': product.desc,
                        'images': [f'{settings.BACKEND_DOMAIN}{product.image.url}']
                    }
                },
                'quantity': quantity
            }

            order_items.append(data)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=order_items,
            metadata={
                "order_id": order.id
            },
            mode='payment',
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL
        )

        return Response({'sessionId': checkout_session['id']}, status=status.HTTP_201_CREATED)


class StripeWebhookAPIView(APIView):
    """
    Stripe webhook API view to handle checkout session completed and other events.
    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret)
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_email = session['customer_details']['email']
            order_id = session['metadata']['order_id']

            print('Payment successfull')

            payment = get_object_or_404(Payment, order=order_id)
            payment.status = 'C'
            payment.save()

            order = get_object_or_404(Order, id=order_id)
            order.status = 'C'
            order.save()

            # TODO - Decrease product quantity

            send_payment_success_email_task.delay(customer_email)

        # Can handle other events here.

        return Response(status=status.HTTP_200_OK)