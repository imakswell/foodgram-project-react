import os
import csv

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """Uploading data from csv file.
    """

    DEFAULT_FILE_PATH = os.path.join(
        os.path.abspath('static/data'),
        'ingredients.csv'
    )

    help = 'Upload data fron csv file to table Ingredients.'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, nargs='?', default=self.DEFAULT_FILE_PATH
        )

    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, unit = row
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=unit)
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded ingredients'))
