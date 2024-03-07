from stateMachines.stateMachine import *
import wpilib
import random

CHANCE_TO_SIGHT = 0.2
CHANCE_TO_JAM = 0.1

LOWER_TIME = 1
RAISE_TIME = 1
STANDBY_TIME = 1

#FOR REFERENCE
#stateMachines\testIntakeDiagram.md
class TestIntakeStateMachine(StateMachine):
    #don't need to include all args because this state machine is predefined in its states/init state
    def __init__(self, debugMode=False, mIntake=None, mPivot=None):
        #init some variables
        self.intake = mIntake
        self.pivot = mPivot

        self.debugTimer = wpilib.Timer()
        self.debugTimer.start()

        states = []

        #create states
        # lowerIntake = State(
        #     name="LowerIntake",
        #     run=lambda: self.pivot.setGroundPickup(),
        #     transition=lambda: "SpinIntakeMotor" if self.intake.isPivotPositioned() else ""
        # )
        # states.append(lowerIntake)
        
        # spinIntakeMotor = State(
        #     name="SpinIntakeMotor",
        #     run=lambda: self.intake.runIntake(0.5),
        #     transition=lambda: "RaiseIntake" if self.timer.advanceIfElapsed(0.5) else ""
        # )
        # states.append(spinIntakeMotor)
        
        # raiseIntake = State(
        #     name="RaiseIntake",
        #     run=lambda: self.intake.setHandOffPickup(),
        #     transition=lambda: "DoneState" if self.intake.isPivotPositioned() else ""
        # )
        # states.append(raiseIntake)

        # doneState = State(
        #     name="DoneState"
        # )
        # states.append(doneState)

        #debug print states
        #keep them here in case you just want a timer and print statements

        #wait until note sighted or command given
        idle = State(
            name="Idle",
            transition=lambda: "Lower" if random.random() < CHANCE_TO_SIGHT else ""
        )
        states.append(idle)

        #lower intake for prep
        lower = State(
            name="Lower",
            enter=lambda: self.debugTimer.reset(),
            transition=lambda: "Standby" if self.debugTimer.advanceIfElapsed(LOWER_TIME) else ""
        )
        states.append(lower)

        #wait until properly aligned
        standby = State(
            name="Standby",
            transition=lambda: "Intake" if self.debugTimer.advanceIfElapsed(STANDBY_TIME) else ""
        )
        states.append(standby)

        #try to intake note
        intake = State(
            name="Intake",
            transition=lambda: "Eject" if random.random() < CHANCE_TO_JAM else "Raise"
        )
        states.append(intake)

        #eject if something is wrong
        eject = State(
            name="Eject",
            transition=lambda: "Idle"
        )
        states.append(eject)

        #raise to handoff position
        #this is when the master machine would tell the shooter
        raiseIntake = State(
            name="Raise",
            enter=lambda: self.debugTimer.reset(),
            transition=lambda: "Wait" if self.debugTimer.advanceIfElapsed(RAISE_TIME) else ""
        )
        states.append(raiseIntake)

        wait = State(
            name="Wait",
            run=lambda: print("Waiting")
        )
        states.append(wait)

        handoff = State(
            name="Handoff",
            enter=lambda: self.debugTimer.reset(),
            transition=lambda:"Idle" if self.debugTimer.advanceIfElapsed(1) else ""
        )
        states.append(handoff)

        # idle
        # lower
        # standby
        # intake
        # eject
        # raise
        # wait
        # handoff
        
        super().__init__(states, None, debugMode)
    
    def enable(self):
        #custom behaviour to reset timer upon being re-enabled
        #should prob reset on disable but idc fix it yourself
        self.debugTimer.reset()
        return super().enable()