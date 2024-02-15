from stateMachines.stateMachine import *
import random
import time
import wpilib

CHANCE_TO_SIGHT = 0.25
CHANCE_TO_STAY = 0.5
CHANCE_FOR_HORRIBLE_ERROR = 0

class IntakeStateMachine(StateMachine):
    def __init__(self, states=[], initialState=None, debugMode=False):

        states = []
    
        #delete this   
        self.debugTimer = wpilib.Timer()

        #lower intake
        lowerIntake = State(
            name="LowerIntake",
            transition=lambda: "PrepIntake" if self.debugTimer.advanceIfElapsed(1) else ""
        )
        states.append(lowerIntake)

        #prepare intake for intaking
        prepIntake = State(
            name="PrepIntake",
            transition=lambda: "SpinIntake" if self.debugTimer.advanceIfElapsed(1) else ""
        )
        states.append(prepIntake)

        #spin intake motors
        spinIntake= State(
            name="SpinIntake",
            transition=lambda: "RaiseIntake" if self.debugTimer.advanceIfElapsed(1) else ""
        )
        states.append(spinIntake)

        #raise intake
        raiseIntake = State(
            name="RaiseIntake",
            transition=lambda: "WaitIntakeHandshake" if self.debugTimer.advanceIfElapsed(1) else ""
        )
        states.append(raiseIntake)

        waitForHandshake = State(
            name="WaitIntakeHandshake"
        )
        states.append(waitForHandshake)

        super().__init__(states, initialState, debugMode)