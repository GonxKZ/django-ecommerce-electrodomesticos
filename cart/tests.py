from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CartItem
from products.models import Product
import json
from unittest.mock import patch, MagicMock

# Crear un mock para el módulo stripe
import sys
from unittest.mock import MagicMock

# Mock del módulo stripe
mock_stripe = MagicMock()
mock_stripe.checkout.Session.create.return_value = MagicMock(id='test_session_id')
mock_stripe.api_key = None
sys.modules['stripe'] = mock_stripe

# Create your tests here.

class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        self.product = Product.objects.create(
            nombre="Lavadora Test",
            descripcion="Una lavadora de prueba",
            precio=299.99,
            destacado=True,
            promocion=False
        )
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
    
    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
    
    def test_get_total(self):
        expected_total = self.product.precio * self.cart_item.quantity
        self.assertEqual(self.cart_item.get_total(), expected_total)

class CartViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        self.product = Product.objects.create(
            nombre="Lavadora Test",
            descripcion="Una lavadora de prueba",
            precio=299.99,
            destacado=True,
            promocion=False
        )
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )
        
        # URLs
        self.cart_detail_url = reverse('cart_detail')
        self.add_to_cart_url = reverse('add_to_cart', args=[self.product.id])
        self.checkout_cod_url = reverse('checkout_cod')
        self.payment_success_url = reverse('payment_success')
        self.create_checkout_session_url = reverse('create_checkout_session')
    
    def test_cart_detail_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart_detail.html')
        self.assertIn('cart_items', response.context)
        self.assertIn('total', response.context)
        self.assertEqual(response.context['total'], 299.99)
    
    def test_cart_detail_view_unauthenticated(self):
        response = self.client.get(self.cart_detail_url)
        self.assertNotEqual(response.status_code, 200)
    
    def test_add_to_cart_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.add_to_cart_url)
        self.assertRedirects(response, reverse('home'))
        
        # Verificar que se incrementó la cantidad
        updated_cart_item = CartItem.objects.get(user=self.user, product=self.product)
        self.assertEqual(updated_cart_item.quantity, 2)
    
    def test_add_to_cart_new_item(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Crear un nuevo producto
        new_product = Product.objects.create(
            nombre="Nevera Test",
            descripcion="Una nevera de prueba",
            precio=499.99,
            destacado=False,
            promocion=True
        )
        
        # Añadir al carrito
        add_url = reverse('add_to_cart', args=[new_product.id])
        response = self.client.get(add_url)
        self.assertRedirects(response, reverse('home'))
        
        # Verificar que se creó un nuevo item
        self.assertTrue(CartItem.objects.filter(user=self.user, product=new_product).exists())
    
    def test_checkout_cod_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.checkout_cod_url)
        self.assertRedirects(response, reverse('home'))
        
        # Verificar que el carrito se vacía
        self.assertEqual(CartItem.objects.filter(user=self.user).count(), 0)
    
    def test_payment_success_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.payment_success_url)
        self.assertRedirects(response, reverse('home'))
        
        # Verificar que el carrito se vacía
        self.assertEqual(CartItem.objects.filter(user=self.user).count(), 0)
    
    def test_create_checkout_session(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.create_checkout_session_url)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], 'test_session_id')
