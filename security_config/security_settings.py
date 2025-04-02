"""
Configuraciones de seguridad recomendadas para Django.
Este archivo contiene las configuraciones recomendadas para mejorar la seguridad
de una aplicación Django.
"""

# Configuraciones de seguridad para settings.py
SECURITY_SETTINGS = {
    # Protección contra CSRF
    'CSRF_COOKIE_SECURE': True,  # Enviar cookie CSRF solo por HTTPS
    'CSRF_COOKIE_HTTPONLY': False,  # JavaScript necesita acceder a la cookie CSRF
    'CSRF_COOKIE_SAMESITE': 'Lax',  # Restricción de SameSite
    
    # Protección de sesiones
    'SESSION_COOKIE_SECURE': True,  # Enviar cookie de sesión solo por HTTPS
    'SESSION_COOKIE_HTTPONLY': True,  # JavaScript no puede acceder a la cookie de sesión
    'SESSION_COOKIE_SAMESITE': 'Lax',  # Restricción de SameSite para sesiones
    
    # Cabeceras de seguridad
    'SECURE_BROWSER_XSS_FILTER': True,  # Activar filtro XSS del navegador
    'SECURE_CONTENT_TYPE_NOSNIFF': True,  # Evitar que el navegador adivine el tipo de contenido
    
    # HTTPS
    'SECURE_SSL_REDIRECT': True,  # Redirigir todas las solicitudes a HTTPS
    'SECURE_HSTS_SECONDS': 31536000,  # HSTS por 1 año
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,  # Incluir subdominios en HSTS
    'SECURE_HSTS_PRELOAD': True,  # Permitir la inclusión en la lista de precarga HSTS
    
    # Configuración para prevenir ataques de clickjacking
    'X_FRAME_OPTIONS': 'DENY',  # Evitar que la página se cargue en un frame
    
    # Content Security Policy
    'CSP_DEFAULT_SRC': ("'self'",),  # Valor predeterminado para todas las directivas
    'CSP_SCRIPT_SRC': ("'self'", "'unsafe-inline'"),  # Fuentes permitidas para scripts
    'CSP_STYLE_SRC': ("'self'", "'unsafe-inline'"),  # Fuentes permitidas para estilos
    'CSP_IMG_SRC': ("'self'", "data:"),  # Fuentes permitidas para imágenes
    'CSP_CONNECT_SRC': ("'self'",),  # Fuentes permitidas para conexiones
    
    # Otras configuraciones de seguridad
    'SECURE_REFERRER_POLICY': 'same-origin',  # Política de referencia
}

# Funciones de ayuda para aplicar configuraciones de seguridad

def apply_security_settings(settings_module):
    """
    Aplica configuraciones de seguridad al módulo de settings de Django.
    
    Args:
        settings_module: El módulo de settings de Django.
    """
    for key, value in SECURITY_SETTINGS.items():
        setattr(settings_module, key, value)

def get_recommended_middleware():
    """
    Devuelve una lista de middleware recomendados para la seguridad.
    
    Returns:
        list: Lista de middleware recomendados.
    """
    return [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # Middleware adicional para CSP
        'csp.middleware.CSPMiddleware',
    ]

def get_password_validators():
    """
    Devuelve una lista de validadores de contraseña recomendados.
    
    Returns:
        list: Lista de diccionarios de configuración para validadores de contraseña.
    """
    return [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 10,
            }
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

def is_debug_mode_safe():
    """
    Verifica si el modo DEBUG es seguro para el entorno actual.
    
    Returns:
        bool: True si el modo DEBUG es seguro, False si no.
    """
    import os
    return os.environ.get('DJANGO_ENV') == 'development'

def get_allowed_hosts():
    """
    Obtiene una lista de hosts permitidos basada en el entorno.
    
    Returns:
        list: Lista de hosts permitidos.
    """
    import os
    env = os.environ.get('DJANGO_ENV', 'production')
    
    if env == 'development':
        return ['localhost', '127.0.0.1', '[::1]']
    elif env == 'staging':
        return ['staging.example.com', '.example.com']
    else:  # production
        return ['.example.com']  # Reemplazar con el dominio real en producción 