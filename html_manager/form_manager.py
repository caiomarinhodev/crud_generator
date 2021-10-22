def get_label(attr):
    LABEL_TAG = '<label>{}</label>'
    return LABEL_TAG.format(str(attr).capitalize())


def get_attributes_display(model, format_type='({})'):
    attributes_model = ['"' + str(f.name) + '"' for f in model._meta.get_fields() if f.editable]
    list_str = ', '.join(map(str, attributes_model))
    format_type = format_type.format(list_str)
    return format_type
