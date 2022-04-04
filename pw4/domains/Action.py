from domains.validator import *


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
            act = Validator(input(f'{self.getprompt_string()} {self._prompt_msg} '),
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

