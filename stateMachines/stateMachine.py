from stateMachines.state import State
import random

class StateMachine():
    def __init__(self, states=None, initialState=None, debugMode=False):
        self.states = states
        self.isActive = True
        self.priorityState = None
        self.lastState = None

        self.debugMode = debugMode
        
        #default to some root state, could be an error handler
        self.rootState = State("ROOT_STATE", transition=lambda: str(initialState if initialState != None else states[0]))
        states.append(self.rootState)

        self.currentState = self.rootState
        self.run()
    
    #mermaid.md
    def run(self):
        """
        Run the current state in the machine.
        """

        if not self.isActive: return

        #if an override state was called, set it to be active
        if self.priorityState:
            self.setState(self.priorityState)
            self.priorityState = None

        try:
            self.currentState.run()
        except Exception:
            print("ERROR! Encountered error while running.")
            self.reset()
            return
        
        #check if a priority state was set during run
        if self.priorityState: return

        newState = self.currentState.getTransition()
        if len(newState) != 0:
            if not self.setState(newState):
                print(f"ERROR! Transition from {self.currentState} to {newState} cannot be found. Check that the state is correctly added or named!")
                self.reset()
        
    def setState(self, state:str):
        """
        Set the current state in the machine.
        """
        for _state in self.states:
            if _state.name == state:
                if self.debugMode: print(f"State changed to {_state}")
                self.currentState = _state

                try:
                    self.currentState.enter()
                except Exception:
                    #return true so we just get the on enter fail
                    print(f"ERROR! On enter in {_state} failed.")
                    self.reset()
                    return True

                return True

        return False
    
    def containsState(self, state):
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
        if self.debugMode: print("Resetting machine to root state.\n")
        self.currentState = self.rootState

    def enable(self):
        """
        Enable the machine
        """
        if self.isActive == False:
            self.isActive = True

            #i hate this
            self.setState(str(self.lastState))
            if self.debugMode: print(f"Restoring state {self.lastState}\n")
            self.lastState = None
    
    def disable(self):
        """
        Disable the machine
        """
        if self.isActive == True:
            self.isActive = False
            self.lastState = self.currentState
            if self.debugMode: print(f"Caching state {self.lastState}\n")
            self.reset()
        
    def addState(self, state):
        """
        Add new state to the machine
        """
        if isinstance(state, State):
            self.states.append(state)
        else:
            print("Please pass a State() object")

    def overrideState(self, state):
        """
        Force a transition to this state (applies on the next StateMachine.run())
        """
        if not self.containsState(state): return
        self.priorityState = state

    @property
    def state(self):
        """
        Get current state
        """
        if self.currentState != None:
            return self.currentState