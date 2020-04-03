from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

from psycopg2.errors import UniqueViolation


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            username = 'admin'
            email = 'admin@admin.ru'
            password = 'admin'
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()

            self.stdout.write(self.style.SUCCESS('Superuser successfully created.'))
        except (UniqueViolation, IntegrityError):
            self.stdout.write(self.style.SUCCESS('Superuser already created.'))