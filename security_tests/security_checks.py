import os
import sys
import subprocess
import json
import re
from datetime import datetime

def run_security_tests():
    """Ejecuta los tests de seguridad y genera un informe."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    # Ejecutar tests de seguridad de Django
    print("Ejecutando tests de seguridad...")
    django_test_result = subprocess.run(
        ["python", "manage.py", "test", "security_tests"],
        capture_output=True,
        text=True
    )
    
    # Analizar salida de los tests
    if django_test_result.returncode == 0:
        results["tests"].append({
            "name": "Django Security Tests",
            "status": "PASS",
            "output": django_test_result.stdout
        })
    else:
        results["tests"].append({
            "name": "Django Security Tests",
            "status": "FAIL",
            "output": django_test_result.stdout + "\n" + django_test_result.stderr
        })
    
    # Verificar configuración de settings.py
    settings_result = check_django_settings()
    results["tests"].append(settings_result)
    
    # Verificar patrones de URL seguros
    urls_result = check_url_patterns()
    results["tests"].append(urls_result)
    
    # Verificar dependencias
    deps_result = check_dependencies()
    results["tests"].append(deps_result)
    
    # Generar informe
    with open("security-report.json", "w") as f:
        json.dump(results, f, indent=2)
        
    # Imprimir resumen
    print("\n=== RESUMEN DE TESTS DE SEGURIDAD ===")
    for test in results["tests"]:
        print(f"{test['name']}: {test['status']}")
    print("======================================")
    
    # Devolver código de salida
    return 0 if all(test["status"] == "PASS" for test in results["tests"]) else 1

def check_django_settings():
    """Verificar configuraciones de seguridad en settings.py."""
    try:
        import django
        from django.conf import settings
        
        issues = []
        
        # Verificar DEBUG
        if settings.DEBUG:
            issues.append("DEBUG está habilitado. Debe estar desactivado en producción.")
        
        # Verificar SECRET_KEY
        if hasattr(settings, 'SECRET_KEY'):
            if len(settings.SECRET_KEY) < 32:
                issues.append("SECRET_KEY es demasiado corta. Debe tener al menos 32 caracteres.")
            if re.match(r'^[a-zA-Z0-9_]+$', settings.SECRET_KEY):
                issues.append("SECRET_KEY es demasiado simple. Debe incluir caracteres especiales.")
        
        # Verificar ALLOWED_HOSTS
        if not settings.ALLOWED_HOSTS or '*' in settings.ALLOWED_HOSTS:
            issues.append("ALLOWED_HOSTS debe estar configurado explícitamente sin usar '*'.")
        
        # Verificar configuraciones de cookies
        if not settings.SESSION_COOKIE_SECURE:
            issues.append("SESSION_COOKIE_SECURE debe estar activado.")
        if not settings.CSRF_COOKIE_SECURE:
            issues.append("CSRF_COOKIE_SECURE debe estar activado.")
        if not settings.SESSION_COOKIE_HTTPONLY:
            issues.append("SESSION_COOKIE_HTTPONLY debe estar activado.")
        
        # Verificar MIDDLEWARE
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        
        for middleware in required_middleware:
            if middleware not in settings.MIDDLEWARE:
                issues.append(f"Falta middleware de seguridad: {middleware}")
        
        if issues:
            return {
                "name": "Django Settings Check",
                "status": "FAIL",
                "issues": issues
            }
        else:
            return {
                "name": "Django Settings Check",
                "status": "PASS"
            }
    except Exception as e:
        return {
            "name": "Django Settings Check",
            "status": "ERROR",
            "error": str(e)
        }

def check_url_patterns():
    """Verificar patrones de URL seguros."""
    try:
        issues = []
        
        # Verificar patrones de URL
        # Esto es un ejemplo muy básico, en la práctica se requiere más análisis
        with open("ecommerce_project/urls.py", "r") as f:
            content = f.read()
            
            # Verificar si se usan expresiones regulares inseguras
            if ".*" in content or ".+" in content:
                issues.append("Se detectaron patrones de URL potencialmente inseguros (.*/.+).")
        
        if issues:
            return {
                "name": "URL Patterns Check",
                "status": "FAIL",
                "issues": issues
            }
        else:
            return {
                "name": "URL Patterns Check",
                "status": "PASS"
            }
    except Exception as e:
        return {
            "name": "URL Patterns Check",
            "status": "ERROR",
            "error": str(e)
        }

def check_dependencies():
    """Verificar dependencias vulnerables."""
    try:
        # Ejecutar safety para verificar dependencias vulnerables
        safety_result = subprocess.run(
            ["pip", "install", "safety"],
            capture_output=True,
            text=True
        )
        
        if safety_result.returncode != 0:
            return {
                "name": "Dependencies Check",
                "status": "ERROR",
                "error": "No se pudo instalar safety."
            }
        
        # Generar requirements para safety
        pip_freeze = subprocess.run(
            ["pip", "freeze"],
            capture_output=True,
            text=True
        )
        
        with open("requirements_freeze.txt", "w") as f:
            f.write(pip_freeze.stdout)
        
        # Ejecutar safety
        safety_check = subprocess.run(
            ["safety", "check", "-r", "requirements_freeze.txt", "--json"],
            capture_output=True,
            text=True
        )
        
        try:
            safety_data = json.loads(safety_check.stdout)
            vulnerabilities = safety_data.get('vulnerabilities', [])
            
            if vulnerabilities:
                return {
                    "name": "Dependencies Check",
                    "status": "FAIL",
                    "issues": [f"{v['name']} {v['installed_version']} - {v['vulnerability']}" for v in vulnerabilities]
                }
            else:
                return {
                    "name": "Dependencies Check",
                    "status": "PASS"
                }
        except json.JSONDecodeError:
            # Si safety no devuelve JSON válido, probablemente no hay vulnerabilidades
            if "No vulnerable packages found" in safety_check.stdout:
                return {
                    "name": "Dependencies Check",
                    "status": "PASS"
                }
            else:
                return {
                    "name": "Dependencies Check",
                    "status": "ERROR",
                    "error": safety_check.stdout
                }
    except Exception as e:
        return {
            "name": "Dependencies Check",
            "status": "ERROR",
            "error": str(e)
        }

if __name__ == "__main__":
    sys.exit(run_security_tests()) 