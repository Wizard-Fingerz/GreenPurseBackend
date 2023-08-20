from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
# from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import NotAcceptable
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from django.utils import timezone
from django.utils.crypto import get_random_string
import datetime
from .managers import UserManager
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
# from django.contrib.auth import get_user_model
from .models import *
from django.dispatch import receiver
from . import signals




# Signal to create a profile when a new user is registered
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save the profile when the user is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email"), max_length=250, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False, verbose_name='Admin')
    is_farmer = models.BooleanField(default=False, verbose_name='Farmer')
    is_agric_enterprise = models.BooleanField(default=False, verbose_name='Agric Enterprise')
    is_customer = models.BooleanField(default=False, verbose_name='Farm Customer')
    phone_number = models.BigIntegerField(unique=True, null=True, blank=True)
    # otp = models.IntegerField(blank=True, null = True)
    # otp_expiry = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # max_otp_try = models.CharField(max_length=2, default= settings.MAX_OTP_TRY)
    # otp_max_out = models.DateTimeField(blank=True, null = True)
    # verified = models.BooleanField(_("verified"), default=False)

    USERNAME_FIELD = 'email'
    
    
    REQUIRED_FIELDS = []
    objects = UserManager()
    class Meta:
        swappable = 'AUTH_USER_MODEL'


    def __str__(self):
        return str(self.first_name) or ''
    
    # Now, connect the signal handlers to the User model
    post_save.connect(create_profile, sender=User)
    post_save.connect(save_profile, sender=User)
    
    # def set_otp_expiry(self):
    #     self.otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
    #     self.save()




class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE
    )
    avatar = models.ImageField(upload_to='avatar', blank=True)
    bio = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return str(self.user.get_full_name())


class Address(models.Model):
    # Address options
    BILLING = 'B'
    SHIPPING = 'S'

    ADDRESS_CHOICES = ((BILLING, _('billing')), (SHIPPING, _('shipping')))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='addresses',
        on_delete=models.CASCADE
    )
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    country = models.CharField(max_length=255)  # Replace with CountryField if desired
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return str(self.user.get_full_name())

