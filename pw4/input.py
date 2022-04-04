from domains.student import *
from domains.course import *
from domains.mark import *
from domains.validator import *
from domains.command import *
from domains.container import *


def addstudents():
    user_input = Validator(input('Input number of students: '), '[0-9]+')
    return user_input.value() if user_input.check() else -1


def addstudentinformation():
    user_input_id = Validator(input('Input student ID: '), '.*')
    user_input_name = Validator(input('Input student name: '), '[A-Za-z][A-Za-z ]*')
    user_input_DoB = Validator(input('Input student DoB: '), '[0-9]{2}/[0-9]{2}/[0-9]{4}')
    if user_input_id.check() and user_input_name.check() and user_input_DoB.check():
        return (user_input_id, user_input_name, user_input_DoB)
    return (None, None, None)


def editstudents():
    n = addstudents()
    if n == -1:
        return False
    for _ in range(n):
        student_id, student_name, student_DoB = editstudents()
        if not (student_id and student_name and student_DoB):
            return False
        Fulllist.students.append(StudentInformation(student_id, student_name, student_DoB))
    return True


def addcourses():
    user_input = Validator(input('Input number of courses: '), '[0-9]+')
    return user_input.value() if user_input.check() else -1


def addcourseinformation():
    user_input_id = Validator(input('Input course ID: '), '.*')
    user_input_name = Validator(input('Input course name: '), '[A-Za-z][A-Za-z ]*')
    user_input_credits = Validator(input('input course credits: '), '[1-9]')
    if user_input_id.check() and user_input_name.check() and user_input_credits.check():
        return (user_input_id.value(), user_input_name.value(), user_input_credits.value())
    return (None, None, None)


def updatemarks(course):
    def input_mark_details():
        print(f'Input marks for the course [{course.getname()}]:')
        for student in Fulllist.students:
            user_input_mark = Validator(
                input(f'Enter mark of student [{student.getname()}]: '), '[0-9.]+')
            if user_input_mark.check():
                value = math.floor(user_input_mark.value(float))
                course.addmark(value, student)
                student.addmark(value, course)
            else:
                return False
    return input_mark_details


def editcourses():
    n = addcourses()
    if n == -1:
        return False
    for _ in range(n):
        course_id, course_name, course_credits = editcourses()
        if not (course_id and course_name and course_credits):
            return False
        Fulllist.courses.append(CourseInformation(course_id, course_name, course_credits))
    return True


def marks():
    acts = ActionList()
    for course in Fulllist.courses:
        acts.add(course.getname(), updatemarks(course))
    acts.add('Return', lambda: -10)
    act1 = CommandPromptAct('Select a course:', acts, f'[1-{acts.getlength()}]')
    act1.main_loop()


def studentsgpa(student):
    def student_gpa():
        print(f'Calculate GPA for student [{student.get_name()}]...')
        student.calculate_gpa()
        print(f'Done, GPA = {student.get_gpa()}')
    return student_gpa()


def calculate_gpa():
    acts = ActionList()
    for student in Fulllist.students:
        acts.add(f'{student.getname()}', studentsgpa(student))
    acts.add('Return to menu', lambda: -10)
    act1 = CommandPromptAct('Select a course:', acts, f'[1-{acts.getlength()}]')
    act1.main_loop()