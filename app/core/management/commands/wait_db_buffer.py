"""
Django management command to wait for the database buffer to be ready.
"""
import time

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Wait for the database buffer to be ready'

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database buffer...')

        is_db_up = False
        while not is_db_up:
            try:
                self.check(databases=['default'])
                is_db_up = True
            except Exception:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is ready!'))
