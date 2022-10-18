import json

from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Tag

User = get_user_model()


def run():
    with open('./data/ingredients.json') as fhand:
        data = json.load(fhand)

        for record in data:
            print(record)
            (Ingredient.objects.
             get_or_create(name=record['name'],
                           measurement_unit=record['measurement_unit']))

    with open('./data/users.json') as fhand:
        data = json.load(fhand)

        for record in data:
            print(record)
            User.objects.get_or_create(username=record['username'],
                                       email=record['email'],
                                       first_name=record['first_name'],
                                       last_name=record['last_name'],
                                       password=record['password'])

    with open('./data/tags.json') as fhand:
        data = json.load(fhand)

        for record in data:
            print(record)
            Tag.objects.get_or_create(name=record['name'],
                                      color=record['color'],
                                      slug=record['slug'])
