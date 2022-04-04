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
