from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def _create_user(self, email, phone_number, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError("Either email or phone number must be provided.")
        
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_customer', True)
        return self._create_user(email=email, phone_number=phone_number, password=password, **extra_fields)
    
    
    def create_farmer_user(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_agric_enterprise', False)
        extra_fields.setdefault('is_customer', False)
        extra_fields.setdefault('is_farmer', True)
        return self._create_user(email=email, phone_number=phone_number, password=password, **extra_fields)
    
    def create_enterprise_user(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_agric_enterprise', True)
        extra_fields.setdefault('is_customer', False)
        extra_fields.setdefault('is_farmer', False)
        return self._create_user(email=email, phone_number=phone_number, password=password, **extra_fields)

    def create_superuser(self, email, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if not email and not phone_number:
            raise ValueError("Either email or phone number must be provided.")
        
        return self._create_user(email=email, phone_number=phone_number, password=password, **extra_fields)
