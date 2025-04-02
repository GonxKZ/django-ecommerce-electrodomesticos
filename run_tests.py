#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner
import sys
from unittest.mock import MagicMock

# Configurar mock para el módulo stripe antes de importar cualquier cosa
if 'stripe' not in sys.modules:
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.create.return_value = MagicMock(id='test_session_id')
    mock_stripe.api_key = None
    sys.modules['stripe'] = mock_stripe

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_project.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["products", "cart", "users"])
    sys.exit(bool(failures)) 