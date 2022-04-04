from domains.mark import *


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
