from django.core.management.base import BaseCommand

from currency.utils import populate_currency_table


class Command(BaseCommand):
    help = 'Fills currency table with initial data such as currencies and their current rates'

    def handle(self, *args, **options):
        populate_currency_table()
        self.stdout.write(self.style.SUCCESS('Successfully populated currency table.'))