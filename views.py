from datetime import date

from my_framework.templator import render
from .patterns.creational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


# controller -  main list
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))

# controller -  main About
class About:
    def __call__(self, request):
        return '200 OK', 'about'

# controller -  Not Found
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', 'PAGE not found look your old and write new views or change request'

# controller -  Shedules

class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-progarmms.html', data=date.today())

# controller -  create course

class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            #метод пост
            data = request['data']

            name  = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)
            return '200 OK', render('course_list.html', object_list=category.courses,
                                    name=category.name, id=category.id)