import os
from csv import DictReader

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
        file_path = options['file_path']
        with open(file_path, encoding='utf-8') as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
        self.stdout.write(
            self.style.SUCCESS(
                f'Data from {file_path}  uploaded successfully'
            )
        )
