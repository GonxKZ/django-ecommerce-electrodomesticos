# Overview de Workflows DevSecOps

Este documento describe los diferentes workflows de CI/CD implementados en el proyecto de e-commerce Django, detallando qué hace cada uno y qué herramientas utiliza.

## 1. CI/CD Pipeline (ci-cd.yml)

**Tipo:** Pipeline principal de Integración Continua y Despliegue Continuo

**Activación:** 
- Push a cualquier rama
- Pull request a cualquier rama
- Manual (workflow_dispatch)

**Qué ejecuta:**
- **Construcción y pruebas (`build-and-test`):**
  - Configuración de Python 3.9
  - Instalación de dependencias desde requirements.txt
  - Ejecución de pruebas unitarias con cobertura
  - Análisis básico de seguridad con Bandit
  - Generación de informes XML de cobertura
  - Almacenamiento de resultados como artefactos

- **Despliegue a desarrollo (`deploy-dev`):**
  - Se ejecuta automáticamente para las ramas `develop` y `feature/security_team7`
  - Realiza el despliegue al entorno de desarrollo (simulado)

- **Despliegue a producción (`deploy-prod`):**
  - Se ejecuta automáticamente para la rama `main` o manualmente
  - Realiza el despliegue al entorno de producción (simulado)

## 2. SAST Security Analysis (sast.yml)

**Tipo:** Análisis Estático de Seguridad de Aplicaciones (SAST)

**Activación:**
- Push a cualquier rama
- Pull request a cualquier rama
- Manual (workflow_dispatch)

**Qué ejecuta:**
- Análisis estático del código con Bandit para identificar vulnerabilidades en Python
- Escaneo de dependencias con Safety para buscar vulnerabilidades conocidas
- Análisis de composición de software con pip-audit
- Análisis avanzado con CodeQL v3 para detección de problemas de seguridad
- Almacenamiento de todos los resultados en un único artefacto

## 3. SCA Pipeline (sca.yml)

**Tipo:** Análisis de Composición de Software (SCA)

**Activación:**
- Push a cualquier rama
- Pull request a cualquier rama
- Manual (workflow_dispatch)

**Qué ejecuta:**
- Análisis completo con Trivy para detectar:
  - Vulnerabilidades en dependencias
  - Problemas en el código fuente
  - CVEs en paquetes de requirements.txt
- Exportación de resultados en formato SARIF para GitHub Security
- Escaneo con Safety para análisis complementario de dependencias
- Análisis detallado con pip-audit para paquetes Python
- Generación de informes en múltiples formatos (JSON, texto plano)
- Integración con GitHub Advanced Security

## 4. Security IaC Pipeline (iac.yml)

**Tipo:** Análisis de Infraestructura como Código (IaC)

**Activación:**
- Push a cualquier rama
- Pull request a cualquier rama
- Manual (workflow_dispatch)

**Qué ejecuta:**
- Análisis con KICS para detectar problemas de seguridad en:
  - Archivos de configuración
  - Definiciones de infraestructura
  - Plantillas y manifiestos
- Análisis de archivos Docker con Hadolint
- Validación de archivos YAML con yamllint
- Revisión de variables de entorno y archivos de configuración sensibles
- Generación de informes detallados con recomendaciones

## 5. Security Tests Pipeline (security-tests.yml)

**Tipo:** Ejecución de Pruebas de Seguridad

**Activación:**
- Push a cualquier rama
- Pull request a cualquier rama
- Manual (workflow_dispatch)

**Qué ejecuta:**
- Búsqueda de pruebas relacionadas con seguridad en el código
- Ejecución específica de tests en el directorio `security_tests`
- Ejecución de tests con nombres relacionados con seguridad en otros directorios
- Medición de cobertura de código para las pruebas de seguridad
- Generación de informes XML y texto de cobertura
- Almacenamiento de resultados como artefactos

## 6. DAST Security Analysis (dast.yml)

**Tipo:** Análisis Dinámico de Seguridad de Aplicaciones (DAST)

**Activación:**
- Push a cualquier rama
- Pull request a cualquier rama
- Manual (workflow_dispatch) con parámetros:
  - URL objetivo
  - Tipo de escaneo
  - Entorno

**Qué ejecuta:**
- Escaneo de seguridad con OWASP ZAP en tres modos posibles:
  - Baseline (rápido, para detección básica)
  - API (específico para APIs)
  - Full (completo, para análisis exhaustivo)
- Análisis de vulnerabilidades web en tiempo de ejecución
- Detección de fallos como XSS, CSRF, inyección SQL, etc.
- Generación de informes en formatos HTML, JSON y Markdown
- Almacenamiento de resultados como artefactos

## 7. DefectDojo Integration (defectdojo-integration.yml)

**Tipo:** Integración con Sistema de Gestión de Vulnerabilidades

**Activación:**
- Después de ejecuciones exitosas de otros workflows de seguridad
- Manual (workflow_dispatch)

**Qué ejecuta:**
- Descarga de artefactos generados por todos los workflows de seguridad
- Organización y consolidación de informes
- Creación automática de engagements en DefectDojo si no existen
- Importación de resultados de seguridad a DefectDojo categorizados por tipo
- Clasificación inteligente de informes según su contenido y extensión
- Proporciona un enlace directo a DefectDojo para revisar los hallazgos

## Interacción entre workflows

Los workflows están diseñados para funcionar tanto de forma independiente como en conjunto:

1. Los workflows de análisis (SAST, SCA, IaC, Tests, DAST) ejecutan diferentes tipos de pruebas de seguridad.
2. Cada workflow genera artefactos con los resultados de sus análisis.
3. El workflow de DefectDojo Integration recopila estos artefactos y los centraliza en un sistema de gestión de vulnerabilidades.
4. El pipeline CI/CD ejecuta pruebas básicas y maneja los despliegues a entornos de desarrollo y producción.

Este enfoque proporciona:
- Seguridad continua en todo el ciclo de vida del desarrollo (DevSecOps)
- Detección temprana de vulnerabilidades
- Gestión centralizada de hallazgos de seguridad
- Despliegue automatizado con controles de seguridad integrados 