"""
Middleware de seguridad para Django.

Este módulo proporciona un middleware para añadir cabeceras de seguridad
a todas las respuestas HTTP en una aplicación Django.
"""

class SecurityHeadersMiddleware:
    """
    Middleware que añade cabeceras de seguridad a las respuestas HTTP.
    
    Estas cabeceras ayudan a proteger contra varios tipos de ataques web
    como XSS, clickjacking, sniffing de contenido, etc.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Procesar la solicitud normalmente
        response = self.get_response(request)
        
        # Añadir cabeceras de seguridad a la respuesta
        
        # Protección contra clickjacking
        if not response.has_header('X-Frame-Options'):
            response['X-Frame-Options'] = 'DENY'
        
        # Prevenir sniffing de MIME types
        if not response.has_header('X-Content-Type-Options'):
            response['X-Content-Type-Options'] = 'nosniff'
        
        # Activar el filtro XSS en navegadores
        if not response.has_header('X-XSS-Protection'):
            response['X-XSS-Protection'] = '1; mode=block'
        
        # Configurar política de referencia
        if not response.has_header('Referrer-Policy'):
            response['Referrer-Policy'] = 'same-origin'
        
        # Añadir Content-Security-Policy básica
        if not response.has_header('Content-Security-Policy'):
            csp_value = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; "
                "connect-src 'self'; "
                "font-src 'self'; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "frame-ancestors 'none'"
            )
            response['Content-Security-Policy'] = csp_value
        
        # Añadir Strict-Transport-Security para HTTPS
        # Solo en producción y solo si la solicitud es HTTPS
        if not request.is_secure():
            # En desarrollo, añadir un encabezado recordatorio
            response['X-Development-Warning'] = 'HSTS no está habilitado en desarrollo'
        elif not response.has_header('Strict-Transport-Security'):
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response 