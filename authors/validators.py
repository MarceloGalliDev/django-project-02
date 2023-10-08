from collections import defaultdict
from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeValidator:
    # assim que estanciamos a classe, já é chamado o método __init__()
    def __init__(self, data, errors=None, ErrorClass=None):
        # se recebermos errors incluiremos dentro de um dicionario
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings
        self.clean_preparation_time()

        cd = self.data

        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self.errors['title'].append('Cannot be equal to description')
            self.errors['description'].append('Cannot be equal to title')

        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_title(self):
        title = self.data.get('title')

        if len(title) < 5:
            self.errors['title'].append('Must have at least 5 chars.')

        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')

        return field_value
