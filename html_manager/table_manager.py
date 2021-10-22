import string


def get_header_table(model, args):
    HEADER_MODEL = ' <th>{}</th> \n'
    Model = model
    attributes_model = [f.name for f in Model._meta.get_fields()]
    header = ""
    for attribute in attributes_model:
        header += HEADER_MODEL.format(str(attribute).upper())
    header = string.Template(header).safe_substitute(**args)
    return header


def get_body_table(model, args):
    BODY_MODEL = ' <td>{}</td> \n'
    Model = model
    attributes_model = [f.name for f in Model._meta.get_fields()]
    body = ""
    for attribute in attributes_model:
        seq = '{{ ${model_name_lower}.'+attribute+' }}'
        body += BODY_MODEL.format(str(seq))
    body = string.Template(body).safe_substitute(**args)
    return body
