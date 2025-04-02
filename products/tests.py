from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product

# Create your tests here.

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            nombre="Lavadora Test",
            descripcion="Una lavadora de prueba",
            precio=299.99,
            destacado=True,
            promocion=False
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.nombre, "Lavadora Test")
        self.assertEqual(self.product.descripcion, "Una lavadora de prueba")
        self.assertEqual(self.product.precio, 299.99)
        self.assertTrue(self.product.destacado)
        self.assertFalse(self.product.promocion)
    
    def test_product_str(self):
        self.assertEqual(str(self.product), "Lavadora Test")

class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product1 = Product.objects.create(
            nombre="Lavadora Destacada",
            descripcion="Una lavadora destacada",
            precio=349.99,
            destacado=True,
            promocion=False
        )
        self.product2 = Product.objects.create(
            nombre="Nevera en Promoción",
            descripcion="Una nevera en promoción",
            precio=499.99,
            destacado=False,
            promocion=True
        )
        self.product_detail_url = reverse('product_detail', args=[self.product1.id])
        self.home_url = reverse('home')
    
    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/home.html')
        self.assertIn('productos_destacados', response.context)
        self.assertIn('promociones', response.context)
        self.assertEqual(len(response.context['productos_destacados']), 1)
        self.assertEqual(len(response.context['promociones']), 1)
        self.assertEqual(response.context['productos_destacados'][0], self.product1)
        self.assertEqual(response.context['promociones'][0], self.product2)
    
    def test_product_detail_view(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], self.product1)
    
    def test_product_detail_view_404(self):
        url = reverse('product_detail', args=[999])  # ID inexistente
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
