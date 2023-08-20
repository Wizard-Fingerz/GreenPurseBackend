from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Transaction
from user.models import User
# from .serializers import (
#     UserSerializer,
#     TransactionSerializer,
#     SummaryByAccountSerializer,
#     SummaryByCategorySerializer,
# )
from .serializers import *
from .custom_classes import SummaryByAccount, SummaryByCategory
from rest_framework.decorators import api_view
from datetime import date
import uuid

# USERS .......................................................................
@csrf_exempt
def users_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def user_detail(request, pk):
    """
    Get user details
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        user.delete()
        return HttpResponse(status=204)


# TRANSACTIONS ................................................................
@csrf_exempt
def transactions_list(request):
    """
    List all transactions, or create a new transaction.
    """
    if request.method == "GET":
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        if type(data) is list:
            for element in data:
                serializer = TransactionSerializer(data=element)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, safe=False, status=201)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def transaction_detail(request, pk):
    """
    Get transaction details

    The primary key of the transaction model is the field reference,
    is necessary to cast the pk to uuid in order to perform the search of the object
    """
    pk = uuid.UUID(pk)
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = TransactionSerializer(transaction)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(transaction, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        transaction.delete()
        return HttpResponse(status=204)


# USER TRANSACTIONS ...........................................................
@api_view(["GET"])
def user_transactions_summary(request, pk):
    start_date = request.query_params.get("start_date", "2000-01-01")
    end_date = request.query_params.get("end_date", date.today())
    type = request.query_params.get("type", None)
    try:
        transactions = Transaction.objects.filter(
            user_id=pk, date__gte=start_date, date__lte=end_date
        )
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)
    if type == "account":
        summary_by_account = SummaryByAccount.fromTransactions(transactions)
        serializer = SummaryByAccountSerializer(summary_by_account, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif type == "category":
        summary_by_category = SummaryByCategory.fromTransactions(transactions)
        serializer = SummaryByCategorySerializer(summary_by_category)
        return JsonResponse(serializer.data, safe=False)
    else:
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse(serializer.errors, status=400)