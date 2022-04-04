import re


class Validator:
    def __init__(self, userinput, accepted_pattern=None):
        self._input = userinput
        self._pattern = re.compile(f'^{accepted_pattern}$')

    def check(self):
        return re.search(self._pattern, self._input)

    def value(self, valuetype=str):
        return valuetype(self._input)
