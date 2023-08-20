from django.contrib import admin
from .models import *


admin.site.register(Wallet)
admin.site.register(Payment)
admin.site.register(WalletTransaction)
