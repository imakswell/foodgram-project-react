import os
import platform

from django.core.management import BaseCommand


class Command(BaseCommand):
    """ Загружает все данные из таблиц в базу данных.
    Названия файлов должны соответствовать CSV_FILE_NAMES.
    Для загрузки данных нужно указать путь к файлу или
    загрузка выполнится автоматически из DEFAULT_FILE_PATH.
    """

    CSV_FILE_NAMES_COMMAND = (
        ('import_ingredients', 'ingredients.csv'),
        ('import_tags', 'tags.csv'),
    )

    DEFAULT_FILE_PATH = os.path.join(
        os.path.abspath('static'), 'data'
    )

    help = 'Upload data to ingredients and tags models'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_dir', type=str, nargs='?', default=''
        )

    def handle(self, *args, **options):
        file_dir = options['file_dir']
        for command, csv_file in self.CSV_FILE_NAMES_COMMAND:
            if file_dir:
                file_path = os.path.join(file_dir, csv_file)
            else:
                file_path = ''
            if platform.system() == 'Windows':
                os.system(f'python manage.py {command} {file_path}')
            else:
                os.system(f'python3 manage.py {command} {file_path}')
