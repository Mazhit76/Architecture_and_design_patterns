from datetime import date
from views import Index, About, StudyPrograms, CategoryList, CopyCourse, CreateCategory, CreateCourse, CoursesList

routes = {
    '/': Index(),
    '/about/': About(),
    '/study_programs/': StudyPrograms(),
    '/courses_list/': CoursesList(),
    '/create_course/': CreateCourse(),
    '/create_category/': CreateCategory(),
    '/category_list/': CategoryList(),
    '/copy_course/': CopyCourse()
}

# front controller
def secret_front(request):
    request['date'] = date.today()

def other_front(request):
    request['key'] = 'key'

fronts = [secret_front, other_front]
