from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import os

def render(template_name, folder='templates', **kwargs):
    env = Environment()
    # указываем папку для поиска шаблонов

    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)

