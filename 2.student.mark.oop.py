import re
import sys
class StudentInformation:
    def __init__(self, student_id, student_name, student_DoB):
        self._id = student_id
        self._name = student_name
        self._DoB = student_DoB

    def getid(self):
        return self._id

    def getname(self):
        return self._name

    def getDoB(self):
        return self._DoB

    def getinfo_header():
        return f'{"ID":^10}{"NAME":^50}{"DATE OF BIRTH":^20}'

    def getinfo(self):
        return f'{self._id:^10}{self._name:>50}{self._dob:^20}'

class CourseInformation:
    def __init__(self, course_id, course_name):
        self._id = course_id
        self._name = course_name
        self._marksheet = MarksheetofCourses()

    def getid(self):
        return self._id

    def getname(self):
        return self._name

    def getinfo_header():
        return f'{"ID":^10}{"NAME":^50}'

    def getinfo(self):
        return f'{self._id:>10}{self._name:>50}'

    def addmark(self, student, mark):
        self._marksheet.update(student, mark)

    def showmarks(self):
        print(MarksheetofCourses.getinfo_header())
        for (student, mark) in self._marksheet.getlist():
            print(f'{student.getname():>50}{mark:^10}')

class MarksheetofCourses:
    def __init__(self):
        self._marksheet = []

    def getinfo_header():
        return f'{"STUDENT NAME":^50}{"MARK":^10}'

    def update(self, student, mark):
        self._marksheet.append((student, mark))
        
    def seemarks(self):
        return bool(self._marksheet)

    def getmark(self, student):
        result = list(filter(lambda x: x[0].getid() == student.getid(), self._marksheet))
        if result:
            return result[0][1]
        return False

    def getlist(self):
        return self._marksheet

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
            print(f'[{i+1}] {desc}')

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
            return self._actlist.getaction(act_num-1)['recall']()
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
                status = self._execute(act.value(int))
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
    return user_input.value(int) if user_input.check() else -1

def addstudentinformation():
    user_input_id = Validator(input('Input student ID: '), '.*')
    user_input_name = Validator(input('Input student name: '), '[A-Za-z][A-Za-z ]*')
    user_input_DoB = Validator(input('Input student DoB: '), '[0-9]{2}/[0-9]{2}/[0-9]{4}')
    if user_input_id.check() and user_input_name.check() and user_input_DoB.check():
        return tuple(map(Validator.value, [user_input_id, user_input_name, user_input_DoB]))
    return (None, None, None)

def addcourses():
    user_input = Validator(input('Input number of courses: '), '[0-9]+')
    return user_input.value(int) if user_input.check() else -1

def addcourseinformation():
    user_input_id = Validator(input('Input course ID: '), '.*')
    user_input_name = Validator(input('Input course name: '), '[A-Za-z][A-Za-z ]*')
    if user_input_id.check() and user_input_name.check():
        return tuple(map(Validator.value, [user_input_id, user_input_name]))
    return (None, None)

def updatemarks(course):
    def input_mark_details():
        print(f'Input marks for the course [{course.getname()}]:')
        for student in Fulllist.students:
            user_input_mark = Validator(
                input(f'Enter mark of student [{student.getname()}]: '),'[0-9.]+')
            if user_input_mark.check():
                course.addmark(student, user_input_mark.value(float))
            else:
                return False
    return input_mark_details

def editstudents():
    n = addstudents()
    if n == -1:
        return False
    for _ in range(n):
        student_id, student_name, student_DoB = editstudents()
        if not (student_id and student_name and student_DoB):
            return False
        Fulllist.students.append(Student(student_id, student_name, student_DoB))
    return True

def editcourses():
    n = addcourses()
    if n == -1:
        return False
    for _ in range(n):
        course_id, course_name = editcourses()
        if not (course_id and course_name):
            return False
        Fulllist.courses.append(Course(course_id, course_name))
    return True

def marks():
    acts = CommandListAct()
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
        print(Student.getinfo_header())
        for student in Fulllist.students:
            print(student.getinfo())
    print()

def courseslist():
    if len(Fulllist.courses) == 0:
        print('Unavailable.')
    else:
        print('List all the courses:')
        print(Course.getinfo_header())
        for course in Fulllist.courses:
            print(course.getinfo())
    print()

def marksinformation(course):
    def editmark():
        print(f"Course [{course.getname()}]'s marksheet:")
        course.showmarks()
    return editmark

def markslist():
    acts = ActionList()
    for course in Fulllist.courses:
        acts.add(course.getname(), editmark(course))
    acts.add('Return', lambda: -10)
    act1 = CommandPromptAct('Select a course:', acts, f'[1-{acts.getlength()}]')
    act1.main_loop()

if __name__ == '__main__':
    act1 = CommandPromptAct('Enter an action:', 
                ActionList([('Enter student info', addstudentinformation),
                ('Enter course info', addcourseinformation),
                ('Enter marks of a course', marks),
                ('Get students', studentslist),
                ('Get courses', courseslist),
                ('Get marks ', markslist),
                ('Exit', lambda: -10)]), '[1-7]')
    act1.main_loop()