class ProgramSuspension: pass

class MsgError:
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class ParseError(MsgError): pass


