from django.test import TestCase
from .models import *
from user.models import *

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.category = Category.objects.create(name='Test Category', description='Test Description')
        self.store = Store.objects.create(userId=self.user, name='Test Store')
        self.product = Product.objects.create(
            title='Test Product',
            description='Test Description',
            storeId=self.store,
            category=self.category,
            price='100.00',
            stock='10',
            condition='New'
        )
        self.product_img = ProductImg.objects.create(productId=self.product, url='https://example.com/image.jpg')
        self.cart = Cart.objects.create(userId=self.user, quantity=1)
        self.cart_item = CartItem.objects.create(cartId=self.cart, productId=self.product, quantity=1)
        self.file_upload = FileUpload.objects.create(cartId='img/test.jpg')
        self.order = Order.objects.create(buyer=self.user, status=Order.PENDING)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1)

    def test_category_creation(self):
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(self.category.name, 'Test Category')

    def test_store_creation(self):
        self.assertEqual(Store.objects.count(), 1)
        self.assertEqual(self.store.name, 'Test Store')

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.title, 'Test Product')

    def test_product_image_creation(self):
        self.assertEqual(ProductImg.objects.count(), 1)
        self.assertEqual(self.product_img.url, 'https://example.com/image.jpg')

    def test_cart_creation(self):
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(self.cart.userId, self.user)

    def test_cart_item_creation(self):
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(self.cart_item.cartId, self.cart)
        self.assertEqual(self.cart_item.productId, self.product)

    def test_file_upload_creation(self):
        self.assertEqual(FileUpload.objects.count(), 1)
        self.assertEqual(str(self.file_upload.cartId), 'img/test.jpg')

    def test_order_creation(self):
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.buyer, self.user)

    def test_order_item_creation(self):
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
