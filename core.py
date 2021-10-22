import codecs
import functools
import operator
import os
import shutil
import string

from django.apps import apps

from django_crud_generator.conf import VIEW_CLASSES, MODULES_TO_INJECT, BASE_TEMPLATES_DIR, ACCOUNTS_LIST_TEMPLATES, \
    LIST_DASHBOARD_DEFAULT_TEMPLATES, LIST_APP_DEFAULT_TEMPLATES, LIST_TEMPLATE_TAGS, LIST_THEME_DEFAULT_TEMPLATES
from django_crud_generator.html_manager.form_manager import get_attributes_display
from django_crud_generator.html_manager.table_manager import get_header_table, get_body_table
from django_crud_generator.utils import convert, check_class_in_file


def get_args(app, model, project_name, type):
    args = {'model_name': str(model.__name__), 'type': str(type),
            'model_prefix': str(model.__name__).upper(),
            'app_name': app, 'url_pattern': str(model.__name__).lower(),
            'project_name': str(project_name)}
    simplified_file_name = convert(str(model.__name__).strip())
    args['simplified_view_file_name'] = simplified_file_name
    args['model_name_lower'] = args['model_name'].lower()
    args['view_file'] = args['simplified_view_file_name']
    args['application_name'] = args['app_name'].split("/")[-1]
    return args


def inject_modules(args):
    for module in MODULES_TO_INJECT:
        generic_insert_module(module, args)
    # render_template_with_args_in_file(
    #     create_or_open(os.path.join(args['app_name'], 'urls.py'), "", args),
    #     os.path.join(BASE_TEMPLATES_DIR, "urls_api_urls_patch.py.tmpl"),
    #     **args
    # )


def add_urls_in_project(args):
    file = create_or_open(os.path.join(args['project_name'], '{}.py'.format('urls')),
                          None,
                          args)
    render_template_with_args_in_file(file,
                                      os.path.join(BASE_TEMPLATES_DIR, '{}.py.tmpl'.format('project_urls')),
                                      **args)
    file.close()


def copy_account_templates(args):
    if not os.path.isdir(os.path.join(args['app_name'], 'templates', 'account')):
        os.mkdir(os.path.join(args['app_name'], 'templates', 'account'))
    for basic in ACCOUNTS_LIST_TEMPLATES:
        original = os.path.join('django_crud_generator', 'base_django', 'templates', args['type'], 'account', basic)
        target = os.path.join(args['app_name'], 'templates', 'account')
        shutil.copy(original, target)


def copy_templates_model(args):
    for type_view in VIEW_CLASSES:
        if not os.path.isdir(os.path.join(args['app_name'], 'templates',
                                          convert(args['model_name'].strip().lower()))):
            os.mkdir(os.path.join(args['app_name'], 'templates',
                                  convert(args['model_name'].strip().lower())))
        original = os.path.join('django_crud_generator', 'base_django', 'templates',
                                args['type'], 'model', convert(type_view.strip().lower() + '.html'))
        target = os.path.join(args['app_name'], 'templates', convert(args['model_name'].strip().lower()),
                              convert(type_view.strip().lower() + '.html'))
        shutil.copy(original, target)


def create_templates_model(args):
    model_name = args['model_name']
    app_name = args['app_name']
    Model = apps.get_model(app_name, model_name)
    args['header_table'] = get_header_table(model=Model, args=args)
    args['body_table'] = get_body_table(model=Model, args=args)
    path_templates_model = os.path.join(app_name, 'templates',
                                        convert(args['model_name'].strip().lower()))
    if not os.path.isdir(path_templates_model):
        os.mkdir(path_templates_model)
    for type_view in VIEW_CLASSES:
        file_path = os.path.join(app_name, 'templates', convert(model_name.strip().lower()),
                                 convert(type_view.strip().lower() + '.html'))
        file_html = create_or_open(file_path, None, None)
        template_path = os.path.join('django_crud_generator', 'base_django', 'templates',
                                     args['type'], 'tmpl', convert(type_view.strip().lower() + '.html.tmpl'))
        render_template_with_args_in_file(
            file_html,
            template_path,
            **args
        )


def copy_templates_default(args):
    list_templates_default = check_default_templates(args)
    for template_item in list_templates_default:
        original = os.path.join('django_crud_generator', 'base_django', 'templates', args['type'],
                                template_item)
        target = os.path.join(args['app_name'], 'templates', template_item)
        shutil.copy(original, target)


def get_theme(args):
    if args['type'] == 'dashboard':
        return 'adminlte'
    elif args['type'] == 'app':
        return 'gromart'
    elif args['type'] == 'store':
        return 'store'
    elif args['type'] == 'default' or args['type'] == 'simple':
        return 'default'
    else:
        return None


def copy_static_theme(args):
    theme = get_theme(args)
    if theme:
        original = os.path.join('django_crud_generator', 'static', theme)
        target = os.path.join('static', theme)
        if not os.path.isdir('static'):
            os.mkdir('static')
        try:
            shutil.copytree(original, target)
        except (FileExistsError,):
            print('-- Theme already exists in STATIC folder.')


def check_default_templates(args):
    if args['type'] == 'dashboard':
        return LIST_DASHBOARD_DEFAULT_TEMPLATES
    elif args['type'] == 'aplicativo':
        return LIST_APP_DEFAULT_TEMPLATES
    return LIST_THEME_DEFAULT_TEMPLATES


def copy_template_tags(args):
    for item in LIST_TEMPLATE_TAGS:
        original = os.path.join('django_crud_generator', 'base_django', 'templatetags', item)
        target = os.path.join(args['app_name'], 'templatetags', item)
        if not os.path.isdir(os.path.join(args['app_name'], 'templatetags')):
            os.mkdir(os.path.join(args['app_name'], 'templatetags'))
            init_file = codecs.open(os.path.join(args['app_name'], 'templatetags', '__init__.py'), 'w+')
            init_file.close()
        shutil.copy(original, target)


def render_template_with_args_in_file(file, template_file_name, **kwargs):
    """
    Get a file and render the content of the template_file_name with kwargs in a file
    :param file: A File Stream to write
    :param template_file_name: path to route with template name
    :param **kwargs: Args to be rendered in template
    """
    template_file_content = "".join(codecs.open(template_file_name, encoding='UTF-8').readlines())
    template_rendered = string.Template(template_file_content).safe_substitute(**kwargs)
    file.write(template_rendered)


def create_or_open(file_name, initial_template_file_name, args):
    """
    Creates a file or open the file with file_name name
    :param file_name: String with a filename
    :param initial_template_file_name: String with path to initial template
    :param args: from console to determine path to save the files
    """
    if not os.path.isfile(file_name):
        file = codecs.open(file_name, 'w+', encoding='UTF-8')
        print("-- Creating {}".format(file_name))
        if initial_template_file_name:
            render_template_with_args_in_file(file, initial_template_file_name, **args)
    else:
        file = codecs.open(file_name, 'a+', encoding='UTF-8')
    return file


def generic_insert_module(module_name, args):
    """
    In general we have a initial template and then insert new data, so we dont repeat the schema for each module
    :param module_name: String with module name
    :paran **kwargs: Args to be rendered in template
    """
    model_name = args['model_name']
    app_name = args['app_name']
    Model = apps.get_model(app_name, model_name)
    args['list_display'] = get_attributes_display(model=Model)
    file = create_or_open(os.path.join(args['app_name'], '{}.py'.format(module_name)),
                          os.path.join(BASE_TEMPLATES_DIR, '{}_initial.py.tmpl'.format(module_name)),
                          args)
    render_template_with_args_in_file(file,
                                      os.path.join(BASE_TEMPLATES_DIR, '{}.py.tmpl'.format(module_name)),
                                      **args)
    file.close()


def generic_insert_with_folder(folder_name, file_name, template_name, checking_classes, args):
    """
    In general if we need to put a file on a folder, we use this method
    """
    # First we make sure views are a package instead a file
    if not os.path.isdir(os.path.join(args['app_name'], folder_name)):
        os.mkdir(os.path.join(args['app_name'], folder_name))
        codecs.open(os.path.join(args['app_name'], folder_name, '__init__.py'), 'w+')
    full_file_name = os.path.join(args['app_name'], folder_name, '{}.py'.format(file_name))
    view_file = create_or_open(full_file_name, '', args)

    if functools.reduce(operator.and_,
                        map(check_class_in_file, (full_file_name,) * len(VIEW_CLASSES), checking_classes)):
        print("-- All classes {} already on file {}".format(", ".join(checking_classes), file_name))
        return 0

    render_template_with_args_in_file(
        view_file,
        os.path.join(
            BASE_TEMPLATES_DIR,
            template_name
        ),
        **args
    )
    view_file.close()
    return 1


def generate_templates_model(args):
    print('-- Generating templates model: ', args['model_name'])
    copy_templates_model(args)


def copy_dependencies(app_name):
    for item in ['requirements.txt', 'Procfile', '.gitignore', 'django.gitlab-ci.yml']:
        original = os.path.join('django_crud_generator', item)
        target = os.path.join(item)
        shutil.copy(original, target)


def delete_all_unused_files():
    list_files = ['views.py', 'tests.py', 'urls.py', 'admin.py', 'forms.py', 'conf.py',
                  'mixins.py', 'serializers.py', 'viewsets.py', 'urls_api.py', 'utils.py']
    for file in list_files:
        path_to_file = os.path.join('app', file)
        if os.path.exists(path_to_file):
            os.remove(path_to_file)
