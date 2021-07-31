from django.test import TestCase, Client, RequestFactory
from unittest import mock
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages.storage.fallback import FallbackStorage
from .models import Category, Notebook, CartProduct, Cart, Customer
from .views import recalc_cart, AddToCartView, BaseView
from decimal import Decimal


User = get_user_model()


class ShopTestCases(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')
        self.category = Category.objects.create(name='Ноутбуки', slug='notebook')
        image = SimpleUploadedFile('notebook_image.jpg', content=b'', content_type='image/jpg')
        self.notebook = Notebook.objects.create(
            category=self.category,
            title='Test Notebook',
            image=image,
            price=Decimal('50000.00'),
            diagonal='17.3',
            display='IPS',
            processor_freq='3.4 GHz',
            ram='6 GB',
            video='GeForce GTX',
            time_without_charge='10 hours',
            slug='test-slug',
        )
        self.customer = Customer.objects.create(user=self.user, phone='111111111', address='Address')
        self.cart = Cart.objects.create(owner=self.customer, final_price=0)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            content_object=self.notebook,
        )
        return super().setUp()

    def test_add_to_cart(self):
        self.cart.product.add(self.cart_product)
        recalc_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.product.all())
        self.assertEqual(self.cart.product.count(), 1)
        self.assertEqual(self.cart.final_price, Decimal('50000.00'))

    def test_response_from_add_to_cart_view(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        setattr(request, 'session', {})
        setattr(request, '_messages', FallbackStorage(request))
        response = AddToCartView.as_view()(request, ct_model='notebook', slug='test-slug')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')

    def test_mock_homepage(self):
        mock_data = mock.Mock(status_code=444)
        with mock.patch('mainapp.views.BaseView.get', return_value=mock_data) as mock_data_:
            factory = RequestFactory()
            request = factory.get('')
            request.user = self.user
            response = BaseView.as_view()(request)
            self.assertEqual(response.status_code, 444)
