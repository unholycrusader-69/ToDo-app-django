#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    import os
    from django.contrib.auth import get_user_model

    if os.environ.get("CREATE_SUPERUSER") == "1":
        import django
        django.setup()
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "yourpassword")
            print("Superuser created successfully.")
        else:
            print("Superuser already exists.")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
