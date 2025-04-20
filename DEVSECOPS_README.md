# Configuración DevSecOps para Django E-commerce

Este documento describe la configuración DevSecOps implementada para el proyecto de e-commerce en Django.

## Componentes Implementados

### 1. Pipeline CI/CD
El workflow `.github/workflows/ci-cd.yml` ejecuta automáticamente:
- Tests unitarios con cobertura
- Análisis estático de seguridad con Bandit

### 2. Análisis de Seguridad Estático (SAST)
El workflow `.github/workflows/sast.yml` realiza:
- Análisis de código con Bandit
- Escaneo de dependencias con Safety
- Análisis de composición de software (SCA) con pip-audit
- Análisis avanzado con CodeQL (si está disponible)

### 3. Análisis de Seguridad Dinámico (DAST)
El workflow `.github/workflows/dast.yml` permite ejecutar:
- Escaneo de seguridad con OWASP ZAP
- Permite diferentes modos de escaneo (baseline, api, full)

### 4. Integración con DefectDojo
El workflow `.github/workflows/defectdojo-integration.yml` se encarga de:
- Importar todos los resultados de seguridad a DefectDojo
- Gestionar vulnerabilidades de forma centralizada

### 5. Middleware de Seguridad
El archivo `security_config/security_middleware.py` implementa:
- Cabeceras de seguridad HTTP
- Protección contra XSS, clickjacking, etc.

## Uso del Sistema

### Ejecutar Workflows Manualmente

#### Pipeline CI/CD
```bash
# Desde GitHub, ir a Actions -> CI/CD Pipeline -> Run workflow
```

#### Análisis SAST
```bash
# Desde GitHub, ir a Actions -> SAST Security Analysis -> Run workflow
```

#### Análisis DAST
```bash
# Desde GitHub, ir a Actions -> DAST Security Analysis -> Run workflow
# Proporcionar la URL objetivo y el tipo de escaneo
```

### Configurar DefectDojo

1. Instalar y configurar DefectDojo según las instrucciones en `CONFIGURACION_DEFECTDOJO.md`

2. Añadir los siguientes secretos a tu repositorio GitHub:
   - `DEFECTDOJO_URL`: URL base de tu instalación DefectDojo
   - `DEFECTDOJO_API_KEY`: Token API generado en DefectDojo
   - `DEFECTDOJO_PRODUCT_ID`: ID del producto en DefectDojo
   - `DEFECTDOJO_ENGAGEMENT_ID`: ID del engagement en DefectDojo

### Integrar el Middleware de Seguridad

Para usar el middleware de seguridad, añade lo siguiente a tu `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Otros middleware...
    'security_config.security_middleware.SecurityHeadersMiddleware',  # Añadir esta línea
]
```

## Mejores Prácticas de Seguridad

1. **Revisión de Código**: Revisar siempre los resultados de los análisis de seguridad
2. **Pull Requests**: Utilizar pull requests para revisar cambios antes de fusionarlos
3. **Gestión de Secretos**: No almacenar credenciales en el código fuente, usar variables de entorno o secretos de GitHub
4. **Actualizaciones**: Mantener las dependencias actualizadas

## Solución de Problemas

### Tests Fallidos
- Verificar que los tests unitarios sean robustos y no dependan de URLs externas
- Usar mocks para servicios externos

### SAST/DAST Fallidos
- Revisar los falsos positivos en los resultados
- Actualizar las reglas de exclusión si es necesario

### Integración con DefectDojo Fallida
- Verificar que las credenciales y los IDs sean correctos
- Comprobar los formatos de los archivos de reporte

## Referencias

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Best Practices](https://docs.djangoproject.com/en/stable/topics/security/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [DefectDojo Documentation](https://defectdojo.github.io/django-DefectDojo/) 