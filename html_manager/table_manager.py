import string

from django.db.models import ManyToOneRel, ManyToManyRel, ManyToManyField

from django_crud_generator.html_manager.form_manager import get_attributes_model


def get_header_table(model, args):
    HEADER_MODEL = ' <th>{}</th> \n'
    attributes_model = [f.name for f in get_attributes_model(model)]
    header = ""
    for attribute in attributes_model:
        header += HEADER_MODEL.format(str(attribute).upper())
    header = string.Template(header).safe_substitute(**args)
    return header


def get_body_table(model, args):
    BODY_MODEL = ' <td>{}</td> \n'
    attributes_model = [f.name for f in get_attributes_model(model)]
    body = ""
    for attribute in attributes_model:
        seq = '{{ ${model_name_lower}.' + attribute + ' }}'
        body += BODY_MODEL.format(str(seq))
    body = string.Template(body).safe_substitute(**args)
    return body
