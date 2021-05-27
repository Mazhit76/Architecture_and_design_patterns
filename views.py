from datetime import date

from my_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavior_patterns import EmailNotifier, SmsNotifier, CreateView, ListView, TemplateView, BaseSerializer

site = Engine()
logger = Logger('main')

email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {}

# controller -  main list
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)

# controller -  main About
@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')



# controller -  Not Found

class NotFound404:
    def __call__(self, request):
        return '404 WHAT', 'PAGE not found look your old and write new views or change request'

# controller -  Shedule
@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study_programs.html', data=date.today())


# controller - list courses
@AppRoute(routes=routes, url='/courses_list/')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# controller -  create course
@AppRoute(routes=routes, url='/create_course/')
class CreateCourse:
    category_id = -1
    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            #метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                #Added observer
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)
            return '200 OK', render('course_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)
        else:

                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)



#controller -copy course
@AppRoute(routes=routes, url='/copy_course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)
                print(name)
            return '200 OK', render('course_list.html', objects_list=site.courses, category=name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'

#controller - edit course
@AppRoute(routes=routes, url='/edit_course/')
class EditCourse:
    category_id = -1
    @Debug(name='EditCourse')
    def __call__(self, request):

        if request['method'] == "POST":
            data = request['data']
            name = data['name']
            old_name = data['old_name']
            name = site.decode_value(name)
            old_name = site.decode_value(old_name)
            if data['id']:
                self.category_id = int(data['id'])
                category = site.find_category_by_id(int(self.category_id))
                course = site.get_course(old_name)
                course.name = name
            return '200 OK', render('course_list.html', objects_list=site.courses, category=category)
      # No  id in POST, and input in data

        else:
            print(request)
            request_params = request['request_params']
            name = request_params['name']
            name = site.decode_value(name)
            self.id_category = request_params['id']
            return '200 OK', render('edit_course.html', old_name=name, name=name, id=self.id_category)

# Controller create category
@AppRoute(routes=routes, url='/create_category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):
        if request['method'] == 'POST':
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


#controller - list categories
@AppRoute(routes=routes, url='/category_list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)

@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'

@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)

@AppRoute(routes=routes, url='/add-students/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site. students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)



@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()