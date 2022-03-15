def addstudents():
    return int(input('Input numbers of students: '))


def addstudentinformation():
    return {'id': input('Input the student id: '),
            'name': input('Input the student name: '),
            'DoB': input('Input students DoB: ')}


def addcourses():
    return int(input('Input numbers of courses: '))


def addcourseinformation():
    return {'id': input('Input the course id: '), 'name': input('Input the course name: ')}


def updatemarks(course):
    print("Input marks for the course {course['name']}: ")
    course['marks'] = []

    for student in students:
        course['marks'].append((student, input("Input the mark of student {student['name']}: ")))


def courseslist():
    print('List all the courses: ')

    for course in courses:
        print("[{course['id']}] {course['name']}", end='')
        print('(mark available)' if 'marks' in course else '')


def studentslist():
    print('List all the students: ')
    print('{"ID":^10} {"DOB":^20} {"NAME":^50}')

    for student in students:
        print("{student['id']:^10} {student['DoB']:^20} {student['name']:^50}")
    print()


def getthecourse(first_message):
    courseslist()
    print(first_message)
    return input('Select a course: ')


def marks(course):
    if 'marks' in course:
        print("Get marks of the course {course['name']}: ")
        print('{"NAME":^20} {"MARK":^5}')
        for student, mark in course['marks']:
            print("{student['name']:<20} {mark:>0}")
    else:
        print('Unavailable')


def findstudents(thislist, key):
    for inputs in thislist:
        if key in inputs.values():
            return inputs
    empty_inputs = thislist[0].copy()
    empty_inputs.clear()
    return empty_inputs


def editStudents():
    print('UPDATE')
    global Studentslist
    print("INPUT ID: ")
    id = input()
    students = findStudents(id)
    if students == False:
        print("NOT FOUND ", id)
    else:
        print("NEW NAME")
        name = input()
        print("NEW DOB:")
        DOB = input()
        students[1]['name'] = name
        students[1]['DOB'] = DOB
        StudentsList[student[0]] = students[1]


if __name__ == '__main__':
    students = []
    courses = []

    for _ in range(addstudents()):
        students.append(addstudentinformation())

    for _ in range(addcourses()):
        courses.append(addcourseinformation())

    studentslist()

