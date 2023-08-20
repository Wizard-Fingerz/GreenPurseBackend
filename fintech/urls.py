from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users_list),
    path('users/<int:pk>/', views.user_detail),
    path('users/<int:pk>/transactions', views.user_transactions_summary),
    path('transactions/', views.transactions_list),
    path('transactions/<str:pk>/', views.transaction_detail),
]