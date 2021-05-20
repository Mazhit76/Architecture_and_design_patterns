from datetime import datetime
# structural patterns  - Decorator for route urls
class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """
        :param cls: Decorator-class, class-url binding
        :return:
        @AppRoute(routes=routes, url='/create-category/')
        """
        self.routes[self.url] = cls()




# structural patterns  - Decorator for time meter
class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        """
        :param cls: Decorator
        :return:
        """
        def timeit(method):
            """ We wrap each class in a time meter"""
            def timed(*args, **kwargs):
                t_s = datetime.now()
                result = method(*args, **kwargs)
                t_e = datetime.now()
                delta = (t_e - t_s).total_seconds()*1000

                print(f'debug--->{self.name} run {delta:2.2f} ms')
                return result
            return timed
        return timeit(cls)
