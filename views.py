from my_framework.templator import render

class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))
class About:
    def __call__(self, request):
        return '200 OK', 'about'
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', 'PAGE not found look your old and write new views or change request'