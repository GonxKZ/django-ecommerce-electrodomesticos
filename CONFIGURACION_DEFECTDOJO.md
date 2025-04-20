# Guía de Configuración de DefectDojo

Esta guía te ayudará a configurar DefectDojo para integrarlo con nuestro pipeline DevSecOps y gestionar las vulnerabilidades detectadas.

## 1. Instalación de DefectDojo

### Opción 1: Instalación con Docker (Recomendada)

1. Clona el repositorio oficial:
   ```bash
   git clone https://github.com/DefectDojo/django-DefectDojo.git
   cd django-DefectDojo
   ```

2. Inicia DefectDojo con Docker Compose:
   ```bash
   ./dc-up.sh
   ```

3. Una vez completada la instalación, accede a DefectDojo en: `http://localhost:8080`
   - Usuario por defecto: `admin`
   - Contraseña por defecto: `admin`

### Opción 2: Instalación en Kubernetes

Si prefieres desplegar DefectDojo en Kubernetes, puedes seguir la [documentación oficial](https://github.com/DefectDojo/django-DefectDojo/blob/master/KUBERNETES.md).

## 2. Configuración Inicial de DefectDojo

### Crear un Tipo de Producto

1. Inicia sesión en DefectDojo
2. Ve a "Configuration" → "Product Types"
3. Haz clic en "Add Product Type"
4. Ingresa la siguiente información:
   - Name: `Django Applications`
   - Description: `Aplicaciones web desarrolladas con Django`
5. Haz clic en "Submit"

### Crear un Producto para la Aplicación

1. Ve a "Products" en el menú principal
2. Haz clic en "Add Product"
3. Ingresa la siguiente información:
   - Name: `django-ecommerce-electrodomesticos`
   - Description: `Aplicación Django para una tienda de electrodomésticos`
   - Product Type: `Django Applications`
   - Product Manager/Team Manager/Technical Contact: Tu información de contacto
4. Haz clic en "Submit"

## 3. Generar API Key para Integración

1. Ve a tu perfil (haz clic en tu nombre de usuario en la esquina superior derecha)
2. Selecciona "API v2 Key"
3. Copia la API Key mostrada (la necesitarás para configurar los secretos de GitHub)

## 4. Configurar Secretos en GitHub

En tu repositorio de GitHub, necesitas configurar el siguiente secreto:

1. Ve a "Settings" → "Secrets" → "Actions"
2. Haz clic en "New repository secret"
3. Configura los siguientes secretos:

   - Nombre: `DEFECTDOJO_URL`
     Valor: URL de tu instancia de DefectDojo (ej. `http://localhost:8080` o `https://defectdojo.tudominio.com`)

   - Nombre: `DEFECTDOJO_API_KEY`
     Valor: La API Key que copiaste en el paso anterior

## 5. Verificar la Integración

Para verificar que la integración funciona correctamente:

1. Ejecuta manualmente el workflow `defectdojo-integration.yml`:
   - Ve a la pestaña "Actions" en GitHub
   - Selecciona "DefectDojo Integration"
   - Haz clic en "Run workflow"
   - Selecciona la rama "develop" o "feature/security_team7"
   - Haz clic en "Run workflow"

2. Una vez completada la ejecución, inicia sesión en DefectDojo y verifica:
   - Deberías ver un nuevo "Engagement" bajo el producto `django-ecommerce-electrodomesticos`
   - Dentro del Engagement, deberías ver los resultados de los escaneos

## 6. Herramientas de Análisis de Seguridad Implementadas

Nuestro pipeline integra varias herramientas de análisis de seguridad:

### SAST (Static Application Security Testing)
- **CodeQL**: Herramienta nativa de GitHub que proporciona análisis de código estático avanzado y detecta vulnerabilidades de seguridad automáticamente. Los resultados se muestran directamente en GitHub en la pestaña "Security" → "Code scanning alerts".
- **Bandit**: Analizador específico para Python que busca problemas de seguridad comunes como inyecciones SQL, manejo inseguro de contraseñas, etc.

### SCA (Software Composition Analysis)
- **OWASP Dependency-Check**: Detecta vulnerabilidades conocidas en las dependencias del proyecto.

### DAST (Dynamic Application Security Testing)
- **OWASP ZAP**: Analiza la aplicación en ejecución para detectar vulnerabilidades dinámicamente.

### Security IaC (Infrastructure as Code)
- **Trivy**: Escanea configuraciones de infraestructura para detectar problemas de seguridad.

## 7. Gestión de Vulnerabilidades en DefectDojo

### Visualizar Vulnerabilidades

1. Ve a "Products" → `django-ecommerce-electrodomesticos`
2. Haz clic en el Engagement más reciente
3. Verás una lista de "Tests" (uno por cada herramienta de escaneo)
4. Haz clic en un Test para ver los hallazgos (vulnerabilidades)

### Verificar Alertas de CodeQL en GitHub

1. Ve a la pestaña "Security" de tu repositorio
2. Haz clic en "Code scanning alerts"
3. Revisa las alertas detectadas por CodeQL

### Priorizar y Asignar Vulnerabilidades

1. En la vista de hallazgos, puedes filtrar por severidad, estado, etc.
2. Para asignar una vulnerabilidad:
   - Haz clic en el hallazgo
   - Haz clic en "Edit"
   - Selecciona el campo "Assignee" y asigna a un miembro del equipo
   - Establece una fecha límite en "Mitigation Date"
   - Haz clic en "Submit"

### Seguimiento de Remediación

1. Cuando una vulnerabilidad se corrige:
   - Haz clic en el hallazgo
   - Cambia el estado a "Mitigated"
   - Añade comentarios sobre cómo se resolvió
   - Haz clic en "Submit"

2. En los siguientes escaneos, DefectDojo detectará si la vulnerabilidad ha sido resuelta y actualizará su estado automáticamente.

## 8. Generar Informes

DefectDojo permite generar diversos tipos de informes:

1. Ve a "Products" → `django-ecommerce-electrodomesticos`
2. Haz clic en "Reports"
3. Selecciona el tipo de informe deseado:
   - Product Type Report
   - Product Security Report
   - Engagement Security Report
   - Test Report
4. Configura las opciones del informe y haz clic en "Generate"

## 9. Solución de Problemas

### Problemas con la Integración CodeQL

Si tienes problemas con CodeQL:
1. Verifica que tu repositorio tenga habilitadas las características de seguridad avanzadas
2. Asegúrate de que los permisos de seguridad estén correctamente configurados en el workflow

### Problemas con la Importación de Resultados

Si los resultados de escaneo no aparecen en DefectDojo:

1. Verifica los logs del workflow en GitHub Actions
2. Asegúrate de que los secretos `DEFECTDOJO_URL` y `DEFECTDOJO_API_KEY` estén configurados correctamente
3. Verifica que la API Key tenga los permisos adecuados en DefectDojo
4. Comprueba que el formato de los resultados convertidos sea compatible con DefectDojo

### Errores en la API

Si obtienes errores de API:

1. Verifica que la URL de DefectDojo sea accesible desde GitHub Actions
2. Confirma que estás usando la API v2 (la v1 está obsoleta)
3. Revisa los logs de DefectDojo para más detalles sobre el error

## 10. Recursos Adicionales

- [Documentación oficial de DefectDojo](https://defectdojo.github.io/django-DefectDojo/)
- [API v2 Documentation](https://defectdojo.github.io/django-DefectDojo/integrations/api-v2-docs/)
- [Integración con CI/CD](https://defectdojo.github.io/django-DefectDojo/integrations/cicd/)
- [Documentación de CodeQL](https://codeql.github.com/docs/)
- [Documentación de Bandit](https://bandit.readthedocs.io/) 