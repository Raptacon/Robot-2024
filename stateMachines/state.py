def testFunc():
    print("Test")

def evalFunc():
    return False

class State():
    def __init__(self, name:str, enter=None, run=None, transition=None, cannotInterupt=False) -> None:
        """
        Defines a state. Takes a name, enter function, and transition function
        """
        self.name = name

        self.onEnter = enter
        self.onRun = run
        self.onTransition = transition
        self.cannotInterupt = cannotInterupt

    def __str__(self) -> str:
        return self.name
    
    def enter(self):
        if not self.onEnter: return
        self.onEnter()
    
    def run(self):
        if self.onRun == None: return
        self.onRun()
    
    def getTransition(self) -> str:
        if self.onTransition == None:
            return ""
        else: 
            return self.onTransition()