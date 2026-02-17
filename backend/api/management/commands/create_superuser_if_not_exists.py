"""
Management command para crear el superusuario inicial si no existe.
Útil para despliegues automatizados en Cloud Run.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import UserProfile


class Command(BaseCommand):
    help = 'Crea el superusuario inicial si no existe'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, default='jeferson.sanchez@csalatam.com')
        parser.add_argument('--password', type=str, default='Col.2023+')
        parser.add_argument('--username', type=str, default='admin')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        username = options['username']

        # Verificar si ya existe
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario con email {email} ya existe.')
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario con username {username} ya existe.')
            )
            return

        # Crear superusuario
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Jeferson',
            last_name='Sanchez'
        )

        # Crear perfil de admin
        UserProfile.objects.create(
            user=user,
            role='admin',
            department='IT'
        )

        self.stdout.write(
            self.style.SUCCESS(f'Superusuario {email} creado exitosamente.')
        )




