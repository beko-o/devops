from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch
from app.models import Product
from django.test import TestCase
class Test(TestCase):
    def test_1(self):
        self.assertEqual(1, 1)
    def test_2(self):
        self.assertEqual(2, 2)
    def test_3(self):
        self.assertEqual(3, 3)
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='This is a test product.',
            price=19.99,
            quantity_available=100,
        )

    def test_product_creation(self):
        """Test whether the product is created correctly."""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.description, 'This is a test product.')
        self.assertEqual(self.product.price, 19.99)
        self.assertEqual(self.product.quantity_available, 100)

    def test_product_str_method(self):
        """Test the __str__ method of the product."""
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_quantity_default(self):
        """quantity_available has a default 0."""
        new_product = Product.objects.create(
            name='Another Test Product',
            description='Another test product description.',
            price=29.99,
        )
        self.assertEqual(new_product.quantity_available, 0)