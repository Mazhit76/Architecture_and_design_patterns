from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

class Requests:
    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            # split parameters by value
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_request_params(environ):
        #         get parameter request
        query_strung = environ['QUERY_STRING']
        #           transform parameter by dict
        request_params = Requests.parse_input_data(query_strung)
        return request_params

    @staticmethod
    def get_wsgi_input_data(environ) -> bytes:
        #         get length request
        content_length_data = environ.get('CONTENT_LENGTH')
        # -> int
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length_data else b''
        return data


class GetRequest(Requests):
    pass
    # def aplication(self, environ, start_response):
    #     """
    #     :param environ: dict data by server
    #     :param start_response: function for server response
    #     :return: b 'string'
    #     """
    #     setup_testing_defaults(environ)
    #     request_params = Requests.get_request_params(environ)
    #     return request_params




class PostRequest:
    def parse_wsgi_input_data(self, data: bytes)->dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = Requests.parse_input_data(data_str)

        return result


    def get_post_request_params(self, environ):
        """
        :param environ: dict data by server
        :return: b 'string'
        """
        # get data
        data = Requests.get_wsgi_input_data(environ)
        # transform data by dict
        data = self.parse_wsgi_input_data(data)

        return data