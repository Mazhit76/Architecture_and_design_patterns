from ..my_framework.templator import render
import jsonpickle

#pattern Observer

class Observer:
    def update(self, subject):
        pass

class SmsNotifier(Observer):
    def update(self, subject):
        print(f' SMS-->  К нам присоеденился {subject.s[-1].name}')

class EmailNotifier(Observer):
    def update(self, subject):
        print(f' Email-->  К нам присоеденился {subject.s[-1].name}')

class Subject:
    def __init__(self):
        self.observers = []
    def notify(self):
        for item in self.observers:
            item.update(self)

class BaseSerializer:
    def __init__(self, obj):
        self.obj = obj
    def save(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)

#pattern Template Method

class TempalateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)
    def __call__(self, request):
        return self.render_template_with_context()

class ListView(TempalateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context

class CreateView(TempalateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            #post
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)

#pattern Strategy

class ConsoleWriter:
    def write(self, text):
        print(text)

class FileWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
