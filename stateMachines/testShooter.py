from stateMachines.stateMachine import *
import wpilib

class TestShooterStateMachine(StateMachine):
    def __init__(self, states=None, initialState=None, debugMode=False, ultraMachine=None):
        
        self.debugTimer = wpilib.Timer()
        self.debugTimer.start()

        states = []
        
        standby = State(
            name="Standby",
        )
        states.append(standby)

        test = State(
            name="Test",
            enter=lambda: self.debugTimer.reset(),
            cannotInterupt=True,
            transition=lambda: "OtherTest" if self.debugTimer.advanceIfElapsed(1) else ""
        )
        states.append(test)

        otherTest = State(
            name="OtherTest",
            enter=lambda: print("done")
        )
        states.append(otherTest)
        
        super().__init__(states, initialState, debugMode)