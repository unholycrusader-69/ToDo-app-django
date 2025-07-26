from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError


class TodoListConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_list'

    def ready(self):
        
        try:
            User = get_user_model()
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="yourpassword"
                )
                print("Superuser 'admin' created automatically.")
        except OperationalError:
            pass
