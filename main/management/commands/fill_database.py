from django.core.management.base import BaseCommand, CommandError
from main.utils.OpenApi import OpenApi
from main.models import Aliment


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if len(Aliment.objects.all()) < 10 * 20:
            OpenApi().fill_database()
