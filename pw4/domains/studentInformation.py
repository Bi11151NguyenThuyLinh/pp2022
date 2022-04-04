import math
import numpy as np
from domains.course import *
from domains.mark import *


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
