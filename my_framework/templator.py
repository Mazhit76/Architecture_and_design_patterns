from jinja2 import Template
import os

def render (tempate_name, folder='templates', **kwargs):
    """
    :param tempate_name: name template
    :param folder: folder in which we are looking template
    :param kwargs: parameters
    :return:
    """

    file_path = os.path.join(folder, tempate_name)

    with open(file_path, encoding='utf-8') as f:
        # read template
        template = Template(f.read())
    #     render template with parameters
    return template.render(**kwargs)