class State():
    #enter, run, transition should prob be callables just so that its expicit in its type
    #but also screw that cause idk what a callable is
    def __init__(self, name:str, enter=None, run=None, transition=None, cannotInterupt=False) -> None:
        """
        State to be used with a finite state machine

        Args:
            Name : Key value to be given to the name. This name is how states will transition to it
            Enter : Evaluated upon entering state. Executed the same tick that it is transitioned to.
            Run : Evaluated every time the state machine is run
            Transition : Must return a string with a name for the state to transition into. Return "" to transition to self
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