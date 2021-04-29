from datetime import date
from views import Index, About

routes = {
    '/': Index(),
    '/about/': About(),
}

# front controller
def secret_front(request):
    request['data'] = date.today()

def other_front(request):
    request['key'] = 'key'

fronts = [secret_front, other_front]
