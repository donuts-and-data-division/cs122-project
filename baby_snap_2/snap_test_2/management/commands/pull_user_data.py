from django.core.management.base import BaseCommand, CommandError
from pull_user_data import get_user_data

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def pull_user_data(self, *args, **options):
        print("Hooray")