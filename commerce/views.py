from django.shortcuts import render
from .serializers import *
from rest_framework.views import *
from rest_framework.decorators import api_view, permission_classes, action
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, filters
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    RetrieveAPIView,
    GenericAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import *
from .permissions import (
    IsOrderByBuyerOrAdmin,
    IsOrderItemByBuyerOrAdmin,
    IsOrderItemPending,
    IsOrderPending
)

import os

# Create your views here.
def product_list(request):
    if request.method == 'GET':
        # products = Product.objects.all().order_by('create_at').reverse()
        products = Product.objects.prefetch_related('product_imgs').order_by('create_at').reverse()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()  # Retrieve all products from the database
        serializer = ProductSerializer(products, many=True)  # Serialize the queryset
        return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
def product_by_id(request, id):
    try:
        product = Product.objects.get(pk=id)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status= 400)
    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status = 201)
        
    
@csrf_exempt
def product_seller(request, storeId):
    try:
        product = Product.objects.get(storeId=storeId)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    
@csrf_exempt
def productImg_list(request):
    if request.method == 'GET':
        productImg = ProductImg.objects.all()
        serializer = ProductImgSerializer(productImgs, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductImgSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)
 
@csrf_exempt
def productImg_product_id(request, productId):
    try:
        productImg = ProductImg.objects.filter(storeId=productId)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = ProductImgSerializer(productImg, many=True)
        return JsonResponse(serializer.data, safe=False)
    

@csrf_exempt
def productImg_by_id(request, id):
    try:
        productImg = ProductImg.objects.get(pk=id)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = ProductImgSerializer(productImg)
        return JsonResponse(serializer.data)
    elif request.method == 'DELETE':
        productImg.delete()
        return HttpResponse(status = 201)

@csrf_exempt
def product_by_category(request, category):
    try:
        product = Product.objects.filter(category=category)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def cart_list(request, category):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)

@csrf_exempt
def cart_by_user_id(request, userId):
    try:
        cart = Cart.objects.filter(userId=userId)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = CartSerializer(cart, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CartSerializer(cart, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status= 400)
    elif request.method == 'DELETE':
        cart.delete()
        return HttpResponse(status = 201)
    
@csrf_exempt
def cart_item_list(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)
  
@csrf_exempt
def cartItem_by_id(request, pk):
    try:
        cartItem = CartItem.objects.get(pk=pk)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = CartItemSerializer(cartItem, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CartItemSerializer(cartItem, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status= 400)
    elif request.method == 'DELETE':
        cartItem.delete()
        return HttpResponse(status = 201)

@csrf_exempt
def cartItem_by_cart(request, cartId):
    try:
        cartItem = CartItem.objects.filter(cartId=cartId)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = CartItemSerializer(cartItem, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def cartItem_by_cart_id(request, cartId):
    try:
        cartItem = CartItem.objects.filter(cartId=cartId)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = CartItemSerializer(cartItem, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def cartItem_detect_same_product(request, cartId, productId):
    try:
        cartItem = CartItem.objects.filter(cartId=cartId).filter(productId=productId)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = CartItemSerializer(cartItem, many=True)
        return JsonResponse(serializer.data, safe=False)

class search_product(generics.ListAPIView):
    search_fields = ('title', 'description', 'category')
    filter_backends = (filters.SearchFilter)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@csrf_exempt
def create_store(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StoreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)
 
@csrf_exempt
def get_store(request, userId):
    try:
        store = Store.objects.filter(userId=userId)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = StoreSerializer(store, many=True)
        return JsonResponse(serializer.data, safe=False)

class upload_file(generics.CreateAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    


def delete_file(request, userId):
    if request.method == 'GET':
        ext = filename.split(".")[-1]
        filenameExt = filename.replace(f'{ext}', "")
        fileDir = "%s/%s.%s" % ("img", filenameExt, ext)
        if os.path.isfile((f'{img}/{filename}')):
            os.remove(fileDir)
            return HttpResponse(f'{filename} deleted')
        return HttpResponse('file not found')


def filter_range_price(request, minprice, maxprice):
    try:
        product = Product.objects.filter(price__range(minprice, maxprice))
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)



def filter_min_price(request, minprice):
    try:
        product = Product.objects.filter(price__gte = minprice)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)



def filter_max_price(request, maxprice):
    try:
        product = Product.objects.filter(price__gte = maxprice)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)



def filter_rating(request, rating):
    try:
        product = Product.objects.filter(rating__gte = rating)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


def filter_condition(request, condition):
    try:
        product = Product.objects.filter(condition = condition)
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


def filter_price_and_rating(request, minprice, maxprice, rating):
    try:
        product = Product.objects.filter(price__range(minprice, maxprice)).filter(rating__gte = rating)
    except:
        return HttpResponse(status= 404)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


def filter_price_and_condition(request, minprice, maxprice, condition):
    try:
        product = Product.objects.filter(price__range(minprice, maxprice)).filter(condition = condition)
    except:
        return HttpResponse(status= 404)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)

def filter_rating_and_condition(request, rating, condition):
    try:
        product = Product.objects.filter(rating__gte = rating).filter(condition = condition)
    except:
        return HttpResponse(status= 404)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


def filter_all(request, minprice, maxprice, rating, condition):
    try:
        product = Product.objects.filter(price__range(minprice, maxprice)).filter(rating__gte = rating).filter(condition = condition)
    except:
        return HttpResponse(status= 404)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)

def get_cart_item_by_cart_id(request, cartId):
    try:
        cartItem = CartItem.objects.filter(cartId=cardId).prefetch_related('productId').order_by('created_at')
    except:
        return HttpResponse(status= 404)
    if request.method == 'GET':
        serializer = JoinSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)
    



class ProductModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()



class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD order items that are associated with the current order id.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsOrderItemByBuyerOrAdmin]

    def get_queryset(self):
        res = super().get_queryset()
        order_id = self.kwargs.get('order_id')
        return res.filter(order__id=order_id)

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        serializer.save(order=order)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes += [IsOrderItemPending]

        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    """
    CRUD orders of a user
    """
    queryset = Order.objects.all()
    permission_classes = [IsOrderByBuyerOrAdmin]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return OrderWriteSerializer

        return OrderReadSerializer

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(buyer=user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes += [IsOrderPending]

        return super().get_permissions()