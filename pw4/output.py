import curses
from domains.student import *
from domains.course import *
from domains.mark import *
from domains.validator import *
from domains.command import *
from domains.container import *


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
    act1 = CommandPromptAct('Enter an action:', ActionList([('Enter student info', addstudentinformation),
                                        ('Enter course info', addcourseinformation),
                                        ('Enter marks of a course', marks),
                                        ('Get students', studentslist),
                                        ('Get courses', courseslist),
                                        ('Get marks ', markslist),
                                        ('Calculate GPA of a student', calculate_gpa),
                                        ('Exit', lambda: -10)]), '[1-7]')
    act1.main_loop()