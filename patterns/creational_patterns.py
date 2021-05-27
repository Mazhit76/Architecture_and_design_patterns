from copy import deepcopy
import quopri
from .behavior_patterns import ConsoleWriter, Subject

# Abctrat user

class User:
    def __init__(self, name):
        self.name = name

# Teacher

class Teacher:
    pass

#Student

class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)

#Generating patern Abstract fabric - fabric users

class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    #generating pattern Fabric metod
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)

# generating pattern Prototype  - course

class CoursePrototype:

    def clone(self):
        return deepcopy(self)

class Course(CoursePrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()  # access Parent variable

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()

#interactive course
class InteractiveCourse(Course):
    pass

#Recording course

class RecordCourse(Course):
    pass


#Category

class Category:

    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count() # possibly a circular link
        return result

# generating pattern Abstract fabric - fabric courses
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }
    #generating pattern Fabric method
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)

#main inerface proekt
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item


    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')

    #generating pattern Singletone for Logger

class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    # @staticmethod
    def log(self, text):
        text = f'log--->', {text}
        self.writer.write(text)
