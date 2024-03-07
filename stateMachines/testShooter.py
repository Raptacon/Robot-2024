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
            transition=lambda: "Wait" if self.debugTimer.advanceIfElapsed(2) else ""
        )
        states.append(test)

        wait = State(
            name="Wait"
        )
        states.append(wait)

        handoff = State(
            name = "Handoff",
            transition=lambda: "PrepFire"
        )
        states.append(handoff)

        prepFire = State(
            name="PrepFire",
            transition=lambda: "Fire"
        )
        states.append(prepFire)

        fire = State(
            name="Fire",
            transition=lambda: "Standby"
        )
        states.append(fire)
        
        super().__init__(states, initialState, debugMode)