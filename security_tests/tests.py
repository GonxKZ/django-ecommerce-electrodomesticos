from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
import re
import os
import json

class SecurityHeadersTest(TestCase):
    """
    Pruebas para verificar que las cabeceras de seguridad están correctamente implementadas.
    """
    def setUp(self):
        self.client = Client()
        # Crear un usuario para probar rutas autenticadas
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='TestPassword123!'
        )
        
    def test_security_headers(self):
        """Verificar que las cabeceras de seguridad HTTP están presentes"""
        response = self.client.get(reverse('home'))
        
        # Content-Security-Policy
        self.assertIn('Content-Security-Policy', response.headers, 
                     "Falta la cabecera Content-Security-Policy")
        
        # X-XSS-Protection
        self.assertIn('X-XSS-Protection', response.headers, 
                     "Falta la cabecera X-XSS-Protection")
        
        # X-Content-Type-Options
        self.assertIn('X-Content-Type-Options', response.headers, 
                     "Falta la cabecera X-Content-Type-Options")
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff',
                        "X-Content-Type-Options debe ser 'nosniff'")
        
        # X-Frame-Options
        self.assertIn('X-Frame-Options', response.headers, 
                     "Falta la cabecera X-Frame-Options")
        
        # Strict-Transport-Security (HSTS)
        self.assertIn('Strict-Transport-Security', response.headers, 
                     "Falta la cabecera HSTS")

class XSSVulnerabilityTest(TestCase):
    """
    Pruebas para detectar vulnerabilidades XSS (Cross-Site Scripting).
    """
    def setUp(self):
        self.client = Client()
        
    def test_xss_protection(self):
        """Probar protección contra XSS en parámetros de URL"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<body onload=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        
        for payload in xss_payloads:
            response = self.client.get(f"/?q={payload}")
            content = response.content.decode('utf-8')
            # Verificar que el payload no se renderiza como HTML sin escapar
            self.assertNotIn(payload, content, 
                            f"Posible vulnerabilidad XSS con payload: {payload}")
            
            # Verificar que los caracteres se escapan correctamente
            self.assertIn("&lt;script&gt;" if "<script>" in payload else payload, content, 
                         f"El payload no se está escapando correctamente: {payload}")

class SQLInjectionTest(TestCase):
    """
    Pruebas para detectar vulnerabilidades de inyección SQL.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='TestPassword123!'
        )
        self.client.login(username='testuser', password='TestPassword123!')
        
    def test_sql_injection_protection(self):
        """Probar protección contra inyección SQL"""
        sql_payloads = [
            "1' OR '1'='1",
            "1; DROP TABLE users;",
            "' UNION SELECT username, password FROM auth_user --",
            "admin'--"
        ]
        
        # Intenta buscar productos con payloads maliciosos
        for payload in sql_payloads:
            response = self.client.get(f"/search/?q={payload}")
            self.assertNotEqual(response.status_code, 500, 
                              f"Error del servidor con payload SQL: {payload}")

class CSRFProtectionTest(TestCase):
    """
    Pruebas para verificar la protección CSRF.
    """
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='TestPassword123!'
        )
        
    def test_csrf_protection(self):
        """Verificar que las solicitudes POST requieren token CSRF"""
        self.client.login(username='testuser', password='TestPassword123!')
        
        # Intenta enviar un formulario sin token CSRF
        response = self.client.post(reverse('profile'), {
            'username': 'testuser_modified',
            'email': 'modified@example.com'
        })
        
        # Debería fallar con 403 Forbidden debido a la falta de token CSRF
        self.assertEqual(response.status_code, 403, 
                        "La solicitud sin token CSRF debería ser rechazada")

class PasswordPolicyTest(TestCase):
    """
    Pruebas para verificar la política de contraseñas.
    """
    def setUp(self):
        self.client = Client()
        
    def test_password_strength(self):
        """Verificar que se aplican políticas de contraseñas fuertes"""
        weak_passwords = [
            "password",
            "123456",
            "qwerty",
            "usuario",
            "admin"
        ]
        
        for password in weak_passwords:
            response = self.client.post(reverse('registro'), {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': password,
                'password2': password
            })
            
            # Si el formulario es válido, la respuesta debería redirigir
            self.assertNotEqual(response.status_code, 302, 
                              f"Contraseña débil aceptada: {password}")

class ConfigurationSecurityTest(TestCase):
    """
    Pruebas para verificar configuraciones de seguridad en Django settings.
    """
    def test_debug_disabled_in_production(self):
        """Verificar que DEBUG está desactivado en producción"""
        if not os.environ.get('DEVELOPMENT'):
            self.assertFalse(settings.DEBUG, 
                            "DEBUG debería estar desactivado en producción")
    
    def test_secure_cookies(self):
        """Verificar que las cookies de sesión son seguras"""
        self.assertTrue(settings.SESSION_COOKIE_SECURE, 
                       "SESSION_COOKIE_SECURE debería estar activado")
        self.assertTrue(settings.CSRF_COOKIE_SECURE, 
                       "CSRF_COOKIE_SECURE debería estar activado")
    
    def test_allowed_hosts(self):
        """Verificar que ALLOWED_HOSTS está correctamente configurado"""
        self.assertNotIn('*', settings.ALLOWED_HOSTS, 
                        "ALLOWED_HOSTS no debe incluir wildcard '*'")
        self.assertNotEqual(settings.ALLOWED_HOSTS, [], 
                           "ALLOWED_HOSTS no debe estar vacío") 