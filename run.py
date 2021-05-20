from my_framework.main import Framework
from urls import fronts
from views import routes
from wsgiref.simple_server import make_server

application = Framework(routes, fronts)

with make_server('', 8081, application) as httpd:
    print('Start on port 8081.....')
    httpd.serve_forever()