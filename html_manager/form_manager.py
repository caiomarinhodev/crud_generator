import string

from django.db.models import ManyToOneRel


def get_label_html(attr):
    LABEL_TAG = '<label>{}</label> \n'
    return LABEL_TAG.format(str(attr).capitalize())


def get_form_html(attr):
    dic = {'attribute': attr}
    form = string.Template('{{ form.${attribute} }} \n').safe_substitute(**dic)
    return form


def make_group_form_html(attr):
    block = get_label_html(attr) + get_form_html(attr)
    dic = {'block': block}
    group = string.Template('<div class="form-group"> \n ${block} </div>').safe_substitute(**dic)
    return group


def make_column_form(attr, length_col=12):
    form_group_attr = make_group_form_html(attr)
    length_col = 'col-xs-' + str(length_col)
    dic = {'block': form_group_attr}
    column = string.Template('<div class="' + length_col + '"> \n ${block} \n </div> \n').safe_substitute(**dic)
    return column


def get_block_form(model):
    attributes_model = [make_column_form(str(f.name)) for f in model._meta.get_fields() if
                        f.editable and str(f.name).lower() != 'id']
    block_form = "".join(map(str, attributes_model))
    return block_form


def get_attributes_display(model, format_type='({})'):
    attributes_model = ['"' + str(f.name) + '"' for f in model._meta.get_fields() if f.editable]
    list_str = ', '.join(map(str, attributes_model))
    format_type = format_type.format(list_str)
    return format_type


def get_list_inlines(model):
    list_attributes_rel = [get_related_name(str(item.related_model)) for item in
                           model._meta.get_fields(include_hidden=True) if
                           type(item) == ManyToOneRel]
    list_inlines = ['{}Inline'.format(attribute) for attribute in list_attributes_rel]
    return list_inlines


def get_inline_classes(model):
    list_inlines = get_list_inlines(model)
    list_inlines = ', '.join(map(str, list_inlines))
    list_inlines = '[{}]'.format(list_inlines)
    return list_inlines


def get_related_name(word):
    return word[word.index('app.models.') + len('app.models.'):word.index("'>")]
