from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django_crud_generator.django_crud_generator import generate_for_model, generate_default_templates, \
    generate_all_models


class Command(BaseCommand):
    help = 'Generate files by models'

    def add_arguments(self, parser):
        parser.add_argument('--app', action='store', type=str)
        parser.add_argument('--model', action='append', type=str)
        parser.add_argument('--default', action='store_true')
        parser.add_argument('--type', action='store', type=str)
        parser.add_argument('--all', action='store_true')

    def handle(self, *args, **kwargs):
        try:
            if 'app' in kwargs:
                name_app = kwargs['app']
            else:
                name_app = 'app'
            if 'type' in kwargs:
                typer = kwargs['type']
            else:
                typer = 'default'
            if kwargs['all']:
                print('-- Generating all templates, files and models')
                generate_default_templates(name_app, typer)
                generate_all_models(name_app, typer)
            else:
                if kwargs['default']:
                    print('-- Creating Default Templates')
                    generate_default_templates(name_app, typer)
                if kwargs['model']:
                    for model in kwargs['model']:
                        model_name = model
                        print('-- Generating model: ', model_name)
                        generate_for_model(name_app, model_name, typer)
        except (Exception,):
            raise CommandError('Error, try again.')
