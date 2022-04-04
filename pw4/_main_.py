from input import *
from output import *


curses.wrapper(curse_splash)
    act1 = CommandPromptAct('Enter an action:',ActionList([('Enter student info', addstudentinformation),
                                        ('Enter course info', addcourseinformation),
                                        ('Enter marks of a course', marks),
                                        ('Get students', studentslist),
                                        ('Get courses', courseslist),
                                        ('Get marks ', markslist),
                                        ('Calculate GPA of a student', calculate_gpa),
                                        ('Exit', lambda: -10)]), '[1-7]')
    act1.main_loop()
