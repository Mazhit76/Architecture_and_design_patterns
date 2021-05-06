# quopri encode and decode strings
import quopri
from .requests import Requests, GetRequest, PostRequest


# not find page
class PageNotFound404:
    def __call__(self, request):
        return '404  WHAT', 'PAGE not found, look your old and write new views or change request'

class Framework:

    """The Foundation frameworks """

    def __init__(self, routes, fronts_obj):
        self.routes = routes
        self.fronts = fronts_obj

    def __call__(self, environ, start_responce):
        # get value PATH_INFO in dictionary environ this is path request
        path = environ['PATH_INFO']

        # added '/' in end path request if not end of line '/' request
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}

        # get all data request
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_post_request_params(environ)
            request['data'] = data
            print(f'Поступил post-запрос: {Framework.decode_value(data)}')

        elif method == 'GET':
            data = GetRequest().get_request_params(environ)
            request['request_params'] = data
            print(f'Нам пришли GET параметры: {data}')

        # assign a handler to the corresponding request adress
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        # fill the dictionary with our handlers
        for front in self.fronts:
            front(request)
        # prepare answer on request
        code, body = view(request)

        start_responce(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        """
            convert the string to bytes by converting ('%'->'=') and ('+'->' ')
        """
        new_data = {}
        for x, y in data.items():
            value = bytes(y.replace('%', '=').replace("+", " "), 'UTF-8')
            value_decode_str = quopri.decodestring(value).decode('UTF-8')
            new_data[x] = value_decode_str
        return new_data