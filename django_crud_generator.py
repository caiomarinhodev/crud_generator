import os

from django.apps import apps

from django_crud_generator.conf import VIEW_CLASSES
from django_crud_generator.core import get_args, generic_insert_with_folder, inject_modules, copy_account_templates, \
    generate_templates_model, copy_template_tags, copy_static_theme, copy_templates_default
from django_crud_generator.utils import check_class_in_file, sanity_check


def generate_all_models(app_name, type='dashboard'):
    models = apps.get_app_config(app_name).get_models()
    for model in models:
        generate_for_model(app_name, model.__name__, type)


def generate_for_model(app_name, model, type='dashboard'):
    model = apps.get_model(app_name, model)
    args = get_args(app_name, model, type)
    models_file_path = os.path.join(args['app_name'], 'models.py')
    if check_class_in_file(models_file_path, str(model.__name__)):
        sanity_check(args)
        generic_insert_with_folder("views", args["simplified_view_file_name"], "view.py.tmpl", VIEW_CLASSES, args)
        permission_class_name = "{}Permission".format(args["model_name"])
        flag = generic_insert_with_folder("tests", "test_{}".format(args["simplified_view_file_name"]), "tests.py.tmpl",
                                          [permission_class_name], args)
        if flag != 0:
            generate_templates_model(args)
            inject_modules(args)


def generate_default_templates(app_name, type='dashboard'):
    args = {'type': type, 'app_name': app_name}
    copy_static_theme(args)
    copy_templates_default(args)
    copy_account_templates(args)
    copy_template_tags(args)
