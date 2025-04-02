# DevSecOps para Django E-Commerce

Este documento describe la configuración DevSecOps implementada para el proyecto de e-commerce en Django ubicado en: https://github.com/GonxKZ/django-ecommerce-electrodomesticos

## Workflows Implementados

### 1. Pipeline CI/CD (ci-cd.yml)
Se ejecuta automáticamente con:
- Cualquier push a cualquier rama
- Cualquier pull request a cualquier rama
- Activación manual desde GitHub Actions

Este workflow realiza:
- Tests unitarios con cobertura
- Análisis estático de seguridad con Bandit
- Despliegue a entornos de desarrollo (para ramas develop y feature/security_team7)
- Despliegue a producción (para rama main o ejecución manual)

### 2. Análisis de Seguridad Estático (sast.yml)
Se ejecuta automáticamente con:
- Cualquier push a cualquier rama
- Cualquier pull request a cualquier rama
- Activación manual desde GitHub Actions

Este workflow realiza:
- Análisis de código con Bandit
- Escaneo de dependencias con Safety
- Análisis de composición de software (SCA) con pip-audit
- Análisis avanzado con CodeQL v3

### 3. Análisis de Composición de Software (sca.yml)
Se ejecuta automáticamente con:
- Cualquier push a cualquier rama
- Cualquier pull request a cualquier rama
- Activación manual desde GitHub Actions

Este workflow realiza:
- Análisis completo con **Trivy** para detectar vulnerabilidades en:
  - Dependencias del proyecto
  - Código fuente
  - Archivos requirements.txt
- Escaneo de dependencias con Safety
- Análisis detallado con pip-audit
- Integración con GitHub Security Dashboard mediante reportes SARIF
- Genera informes en múltiples formatos

### 4. Análisis de Infraestructura como Código (iac.yml)
Se ejecuta automáticamente con:
- Cualquier push a cualquier rama
- Cualquier pull request a cualquier rama
- Activación manual desde GitHub Actions

Este workflow realiza:
- Análisis con **KICS** (Keeping Infrastructure as Code Secure) para detectar problemas en:
  - Archivos de configuración
  - Definiciones de infraestructura
  - Scripts y manifiestos
- Análisis de archivos Docker con Hadolint
- Validación de archivos YAML con yamllint
- Revisión de variables de entorno y configuraciones

### 5. Pruebas de Seguridad (security-tests.yml)
Se ejecuta automáticamente con:
- Cualquier push a cualquier rama
- Cualquier pull request a cualquier rama
- Activación manual desde GitHub Actions

Este workflow realiza:
- Ejecución de tests específicos de seguridad
- Medición de cobertura de pruebas de seguridad
- Genera informes detallados de resultados

### 6. Análisis de Seguridad Dinámico (dast.yml)
Se ejecuta automáticamente con pushes y PRs, y también permite la ejecución manual con parámetros:
- URL objetivo a analizar
- Tipo de escaneo (baseline, api, full)
- Entorno a analizar

Este workflow realiza:
- Escaneo de seguridad con OWASP ZAP
- Análisis de vulnerabilidades web en tiempo de ejecución
- Genera informes detallados de resultados

### 7. Integración con DefectDojo (defectdojo-integration.yml)
Se ejecuta automáticamente:
- Después de cada ejecución exitosa de SAST o CI/CD
- También se puede activar manualmente

Este workflow:
- Recopila los resultados de seguridad de los workflows anteriores
- Los importa a DefectDojo (si está configurado)

## Uso del Sistema

### Ejecución Automática
Todos los workflows se ejecutan automáticamente en cada push y pull request a cualquier rama.

### Ejecución Manual

Los workflows también se pueden ejecutar manualmente:

1. Ve a la pestaña "Actions" en tu repositorio: https://github.com/GonxKZ/django-ecommerce-electrodomesticos/actions
2. Selecciona el workflow que deseas ejecutar
3. Haz clic en "Run workflow"
4. Selecciona la rama en la que deseas ejecutarlo
5. Haz clic en "Run workflow"

#### Para DAST (Análisis Dinámico)
1. Ve a "Actions" > "DAST Security Analysis"
2. Haz clic en "Run workflow"
3. Proporciona la URL objetivo (por defecto es localhost:8000)
4. Selecciona el tipo de escaneo: baseline (rápido), api, o full (completo)
5. Selecciona el entorno: desarrollo, producción, staging, otro
6. Haz clic en "Run workflow"

### Configurar DefectDojo

Para que la integración con DefectDojo funcione, debes añadir estos secretos en tu repositorio:

1. Ve a "Settings" > "Secrets and variables" > "Actions"
2. Añade los siguientes secretos:
   - `DEFECTDOJO_URL`: URL base de tu instalación DefectDojo
   - `DEFECTDOJO_API_KEY`: Token API generado en DefectDojo
   - `DEFECTDOJO_PRODUCT_ID`: ID del producto en DefectDojo
   - `DEFECTDOJO_ENGAGEMENT_ID`: ID del engagement en DefectDojo

## Visualización de Resultados

### Resultados de cada Workflow
1. Ve a "Actions" > Selecciona la ejecución del workflow
2. Baja hasta "Artifacts"
3. Descarga los artefactos para ver los informes detallados:
   - `security-analysis`: Resultados del pipeline CI/CD
   - `security-scan-results`: Resultados del análisis SAST
   - `sca-reports`: Resultados del análisis de dependencias con Trivy, Safety y pip-audit
   - `iac-reports`: Resultados del análisis de infraestructura con KICS y otras herramientas
   - `security-test-reports`: Resultados de las pruebas de seguridad
   - `dast-reports`: Resultados del análisis dinámico

### Resultados en GitHub Security
Los resultados de Trivy se integran con GitHub Security Dashboard, permitiendo ver las vulnerabilidades directamente en GitHub (si tienes habilitada la funcionalidad de GitHub Advanced Security).

### Resultados en DefectDojo
Si has configurado la integración con DefectDojo:
1. Accede a tu instancia de DefectDojo
2. Ve al producto y engagement que configuraste
3. Revisa los hallazgos importados automáticamente desde los workflows

## Herramientas de Seguridad Integradas

### KICS (Keeping Infrastructure as Code Secure)
KICS es una herramienta de análisis estático para infraestructura como código que permite identificar problemas de seguridad, cumplimiento y buenas prácticas en archivos de configuración. Analiza una amplia variedad de plataformas y frameworks como:
- Terraform, CloudFormation, Kubernetes
- Docker, Ansible, Serverless
- Archivos de configuración generales

### Trivy
Trivy es un escáner completo de vulnerabilidades para múltiples componentes:
- Dependencias (Python, Node.js, Java, etc.)
- Imágenes de contenedores
- Código fuente
- Configuraciones y archivos IaC
- Sistemas de archivos completos

Trivy genera informes detallados con referencias a bases de datos de vulnerabilidades como CVE, ayudando a priorizar las mitigaciones.

## Solución de Problemas

### Workflow fallando
- Verifica los logs en la pestaña "Actions"
- Asegúrate de que todas las dependencias están correctamente instaladas
- Comprueba que los tests no dependan de URLs externas

### Errores de CodeQL
- Si hay errores relacionados con versiones obsoletas, se han actualizado a v3
- Verifica que el repositorio tenga los permisos adecuados

### DAST no genera informes
- Asegúrate de que la URL objetivo sea accesible
- Ejecuta manualmente el workflow con parámetros específicos

### Integración con DefectDojo fallando
- Verifica que los secretos están correctamente configurados
- Comprueba que los IDs de producto y engagement son válidos
- Revisa los logs del workflow para ver mensajes de error específicos

### Problemas con KICS o Trivy
- Asegúrate de que los permisos del repositorio permiten acciones de escritura para security-events
- Revisa los logs de ejecución para ver mensajes de error específicos
- Para Trivy, verifica que el archivo requirements.txt está en el formato correcto

## Referencias

- [GitHub Actions Documentation](https://docs.github.com/es/actions)
- [OWASP ZAP](https://www.zaproxy.org/)
- [DefectDojo](https://defectdojo.github.io/django-DefectDojo/)
- [Bandit](https://bandit.readthedocs.io/)
- [Safety](https://pyup.io/safety/)
- [CodeQL](https://codeql.github.com/)
- [KICS](https://kics.io/index.html)
- [Trivy](https://trivy.dev/latest/) 