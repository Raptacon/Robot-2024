from stateMachines.stateMachine import *

class TestShooterStateMachine(StateMachine):
    def __init__(self, states=None, initialState=None, debugMode=False, ultraMachine=None):
        states = []
        
        standby = State(
            name="Standby",
        )
        states.append(standby)

        test = State(
            name="Test",
            run=lambda: print("Yay")
        )
        states.append(test)
        
        super().__init__(states, initialState, debugMode)