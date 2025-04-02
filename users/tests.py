from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import LoginForm, RegistroForm, UserUpdateForm, ProfileUpdateForm

# Create your tests here.

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        self.profile = UserProfile.objects.get(user=self.user)
        
        # Actualizar datos del perfil
        self.profile.direccion_envio = "Calle Test 123"
        self.profile.ciudad_envio = "Ciudad Test"
        self.profile.codigo_postal_envio = "12345"
        self.profile.telefono = "666777888"
        self.profile.save()
    
    def test_profile_creation(self):
        # Verificar que se creó automáticamente con la señal
        self.assertEqual(UserProfile.objects.count(), 1)
    
    def test_profile_update(self):
        self.assertEqual(self.profile.direccion_envio, "Calle Test 123")
        self.assertEqual(self.profile.ciudad_envio, "Ciudad Test")
        self.assertEqual(self.profile.codigo_postal_envio, "12345")
        self.assertEqual(self.profile.telefono, "666777888")
    
    def test_profile_str(self):
        expected_str = f"Perfil de {self.user.username}"
        self.assertEqual(str(self.profile), expected_str)

class UserFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
    
    def test_login_form_valid(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registro_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        form = RegistroForm(data=form_data)
        self.assertTrue(form.is_valid())

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.registro_url = reverse('registro')
        self.profile_url = reverse('profile')
    
    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)
    
    def test_login_view_post_valid(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, form_data)
        self.assertRedirects(response, reverse('home'))
    
    def test_login_view_post_invalid(self):
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_login_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, reverse('home'))
    
    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, reverse('home'))
        
        # Verificar que el usuario ya no está autenticado
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)
    
    def test_registro_view_get(self):
        response = self.client.get(self.registro_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registro.html')
        self.assertIsInstance(response.context['form'], RegistroForm)
    
    def test_registro_view_post_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        response = self.client.post(self.registro_url, form_data)
        self.assertRedirects(response, reverse('home'))
        
        # Verificar que se creó el usuario
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Verificar que se creó el perfil
        user = User.objects.get(username='newuser')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
    
    def test_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsInstance(response.context['user_form'], UserUpdateForm)
        self.assertIsInstance(response.context['profile_form'], ProfileUpdateForm)
    
    def test_profile_view_post_valid(self):
        self.client.login(username='testuser', password='testpassword')
        
        form_data = {
            'username': 'testuser_updated',
            'email': 'updated@example.com',
            'direccion_envio': 'Nueva dirección',
            'ciudad_envio': 'Nueva ciudad',
            'codigo_postal_envio': '54321',
            'telefono': '999888777'
        }
        
        response = self.client.post(self.profile_url, form_data)
        self.assertRedirects(response, self.profile_url)
        
        # Refrescar el usuario desde la base de datos
        self.user.refresh_from_db()
        user_profile = UserProfile.objects.get(user=self.user)
        
        # Verificar que los datos se actualizaron
        self.assertEqual(self.user.username, 'testuser_updated')
        self.assertEqual(self.user.email, 'updated@example.com')
