#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import socket

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCrudMongoDB.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Obtener la dirección IP actual
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os.environ['DJANGO_DEBUG'] = 'True'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoCrudMongoDB.settings'
    execute_from_command_line(['manage.py', 'runserver', '{}:8000'.format(ip_address)])


if __name__ == '__main__':
    main()
