import re
import sys
import math
import curses
import numpy as np


class MarkSheet:
    class Mark:
        def __init__(self, value, return_obj=None, input_obj=None):
            self._value = value
            self._manager = return_obj
            self._input = input_obj

        def getvalue(self):
            return self._value

        def getobject(self, _type):
            if isinstance(self._manager, _type):
                return self._manager
            return self._input

    def __init__(self):
        self._marks = []

    def addmark(self, value, obj=None):
        mark = MarkSheet.Mark(value, input_obj=obj)
        self._marks.append(mark)

    def getmark(self, obj=None):
        for mark in self._marks:
            if mark.getobject(obj.__class__) == obj:
                return mark
        return False

    def seemarks(self):
        return bool(self._marks)


class StudentInformation(MarkSheet):
    def __init__(self, student_id, student_name, student_DoB):
        self._id = student_id
        self._name = student_name
        self._DoB = student_DoB
        self._gpa = None
        super().__init__()

    def getid(self):
        return self._id

    def getname(self):
        return self._name

    def getDoB(self):
        return self._DoB

    def get_gpa(self):
        return self._gpa

    def _pre_gpa(self):
        self._credits = []
        self._gpa_values = []
        for mark in self._marks:
            self._credits.append(mark.getobject(CourseInformation).getcredits())
            self._gpa_values.append(mark.getvalue())

    def getgpa(self):
        self._pre_gpa()
        self._gpa = math.floor(np.average(np.array(self._gpa_values), weights=np.array(self._credits)))


class CourseInformation(MarkSheet):
    def __init__(self, course_id, course_name, course_credits):
        self._id = course_id
        self._name = course_name
        self._credits = course_credits
        super().__init__()

    def getid(self):
        return self._id

    def getname(self):
        return self._name

    def getcredits(self):
        return self._credits

    def showmarks(self):
        return self._marks


class Validator:
    def __init__(self, userinput, accepted_pattern=None):
        self._input = userinput
        self._pattern = re.compile(f'^{accepted_pattern}$')

    def check(self):
        return re.search(self._pattern, self._input)

    def value(self, valuetype=str):
        return valuetype(self._input)


class ActionList:
    def __init__(self, actlist=None):
        self._actlist = []
        if actlist and isinstance(actlist, list):
            for act_desc, act_recall in actlist:
                self.add(act_desc, act_recall)

    def add(self, act_desc, act_recall):
        actvalidator = Validator(act_desc, '[A-Za-z][A-Za-z\'" ]+')
        if actvalidator.check() and callable(act_recall):
            self._actlist.append({'desc': act_desc, 'recall': act_recall})
        else:
            raise Exception("Can't add action anymore.")

    def list_actions(self):
        for i in range(len(self._actlist)):
            desc = self._actlist[i]['desc']
            print(f'[{i + 1}] {desc}')

    def getaction(self, act_num):
        return self._actlist[act_num]

    def getlength(self):
        return len(self._actlist)


class CommandPromptAct:
    state = -1

    def __init__(self, msg, actlist=None, pattern=None):
        self._prompt_msg = msg
        self._actlist = actlist
        self._accepted_command_pattern = pattern
        self._PS = ['>>>', '->', '--->']
        CommandPromptAct.state += 1

    def _list_actions(self):
        self._actlist.list_actions()

    def _execute(self, act_num):
        try:
            return self._actlist.getaction(act_num - 1)['recall']()
        except:
            print(f'Error: {sys.exc_info()}')

    def getprompt_string(self):
        return self._PS[CommandPromptAct.state]

    def main_loop(self):
        while True:
            self._list_actions()
            act = Validator(
                input(f'{self.getprompt_string()} {self._prompt_msg} '),
                accepted_pattern=self._accepted_command_pattern)
            if act.check():
                status = self._execute(act.value())
                if status == -10:
                    CommandPromptAct.state -= 1
                    break
                elif status == False:
                    print('Error: Invalid Value.')
                else:
                    print('Error: Invalid action')


class Fulllist:
    students = []
    courses = []


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


def studentslist():
    if len(Fulllist.students) == 0:
        print('Unavailable.')
    else:
        print('List all the students:')
        print(f'{"ID":^10}{"NAME":^50}{"DATE OF BIRTH":^20}{"GPA":^5}')
        for student in Fulllist.students:
            info = f'{student.getid():^10}'
            info += f'{student.getname():>50}'
            info += f'{student.getDoB():^20}'
            info += f'{(student.getgpa() if student.getgpa() else "other"):>5}'
            print(info)
    print()


def courseslist():
    if len(Fulllist.courses) == 0:
        print('Unavailable.')
    else:
        print('List all the courses:')
        print(f'{"ID":^10}{"NAME":^50}{"CREDITS":^5}{"GRADED":^10}')
        for course in Fulllist.courses:
            info = f'{course.getid():>10}'
            info += f'{course.getname():>50}'
            info += f'{course.getcredits():>5}'
            info += f'{course.seemarks():^10}'
            print(info)
    print()


def marksinformation(course):
    def editmark():
        print(f"Course [{course.getname()}]'s marksheet:")
        print(f'{"STUDENT NAME":^50}{"MARK":^10}')
        for mark in course.showmarks():
            student = mark.getobject(StudentInformation)
            print(f'{student.getname():<20}{mark.getvalue():^10}')
    return editmark


def markslist():
    acts = ActionList()
    for course in Fulllist.courses:
        acts.add(course.getname(), marksinformation(course))
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


def curse_splash(stdscr):
    stdscr.border('|', '|', '-', '-', '+', '+', '+', '+')
    s = "Curses is still in development..."
    stdscr.addstr(curses.LINES//2-1, curses.COLS//2-len(s)//2, s)
    s = "Press any key to continue in CLI mode"
    stdscr.addstr(curses.LINES//2+1, curses.COLS//2-len(s)//2, s)
    curses.curs_set(0)
    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    curses.wrapper(curse_splash)
    act1 = CommandPromptAct('Enter an action:',
                            ActionList([('Enter student info', addstudentinformation),
                                        ('Enter course info', addcourseinformation),
                                        ('Enter marks of a course', marks),
                                        ('Get students', studentslist),
                                        ('Get courses', courseslist),
                                        ('Get marks ', markslist),
                                        ('Calculate GPA of a student', calculate_gpa),
                                        ('Exit', lambda: -10)]), '[1-7]')
    act1.main_loop()