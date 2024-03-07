from stateMachines.state import State

class StateMachine():
    def __init__(self, states=None, initialState=None, debugMode=False):
        """
        Finite state machine that uses string-state dictionaries

        Args:
            States : a list of states
            Initial state : the state to which the root state connects
            Debug mode : If true, allows for print statements when switching states or enabling/disabling state machine
        """
        self.states = states
        self.isActive = False
        self.lastState = None

        self.debugMode = debugMode
        
        #default to some root state, could be an error handler
        self.rootState = State("ROOT_STATE", transition=lambda: str(initialState if initialState != None else states[0]))
        states.append(self.rootState)

        self.currentState = self.rootState
        
    #mermaid.md
    def run(self) -> bool:
        """
        Run the current state in the machine.

        Returns:
            True -> Success
            
            False -> Error or invalid transition
        """

        if not self.isActive: return

        #attempt to run current state
        try:
            self.currentState.run()
        except Exception:
            #return false if failure
            self.say("ERROR! Encountered error while running.")
            self.reset()
            return False

        #evaluate transition of state
        newState = self.currentState.getTransition()
        if len(newState) != 0:
            setStateStatus = self.setState(newState)
            if not setStateStatus:
                #force a reset if status returns false
                self.say(f"ERROR! Transition from {self.currentState} to {newState} cannot be found. Check that the state is correctly added or named!")
                self.reset()
    
            return setStateStatus

        return True
        
    def setState(self, state:str) -> bool:
        """
        Set the current state in the machine. Does not care about whether it is interuptable
        """
        for _state in self.states:
            if _state.name == state:
                if self.debugMode: self.say(f"State changed to {_state}")
                self.currentState = _state
                
                try:
                    self.currentState.enter()
                except Exception:
                    #return true so we just get the on enter fail
                    self.say(f"ERROR! On enter in {_state} failed.")
                    self.reset()
                    return True

                return True

        return False
    
    def containsState(self, state:str):
        """
        Check if a state with the given name exists
        """
        for _state in self.states:
            if _state.name == state:
                return True
        return False
    
    def reset(self):
        """
        Reset the state to the root (transitions to whatever state[0] was if not defined)
        """
        if self.debugMode: self.say("Resetting machine to root state.\n")
        self.currentState = self.rootState

    def enable(self):
        """
        Enable the machine. This must be called after creating a machine.
        """
        if self.isActive == False:
            self.isActive = True
        
            #i hate this
            if self.lastState != None:
                self.setState(str(self.lastState))
                if self.debugMode: self.say(f"Restoring state {self.lastState}\n")
                self.lastState = None
    
    def disable(self):
        """
        Disable the machine
        """
        if self.isActive == True:
            self.isActive = False
            self.lastState = self.currentState
            if self.debugMode: self.say(f"Caching state {self.lastState}\n")
            self.reset()
        
    def addState(self, state):
        """
        Add new state to the machine
        """
        if isinstance(state, State):
            self.states.append(state)
        else:
            self.say("Please pass a State() object")
    
    #this is probably a dumb name.
    #will come up with something better later
    def overrideState(self, state):
        """
        Force a transition to this state
        """
        #check we aren't forcing a transition to the current state
        if state == str(self.currentState): return

        #check state exists
        if not self.containsState(state):
            self.say("Requested overrided state not found.")
            return
        
        #check state cannot be interupted
        if self.currentState.cannotInterupt == True:
            self.say(f"Current state, {self.currentState}, is set to uninteruptable. Use setState() if you don't care")
            return
        
        self.say(f"Forcing transition to {state}.")
        self.setState(state)
    
    def say(self, message:str):
        """
        Print statement with class name in front. 
        """
        print(f"{self.__class__.__name__}: {message}")

    @property
    def state(self):
        """
        Current state of machine
        """
        if self.currentState != None:
            return self.currentState