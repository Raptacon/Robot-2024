from stateMachines.stateMachine import *
import wpilib
import random
from subsystem.sparkyIntake import SparkyIntake
from subsystem.sparkyIntakePivotController import *

CHANCE_TO_SIGHT = 0.2
CHANCE_TO_JAM = 0.1

LOWER_TIME = 2
RAISE_TIME = .3
STANDBY_TIME = 4

#FOR REFERENCE
#stateMachines\testIntakeDiagram.md
class TestIntakeStateMachine(StateMachine):
    #don't need to include all args because this state machine is predefined in its states/init state
    def __init__(self, intake:SparkyIntake, pivot:pivotController, debugMode=False):
        #init some variables
        if intake == None or pivot == None:
            raise Exception("Intake state machine intake and pivot references not given.")
        
        self.intake = intake
        self.pivotController = pivot
        
        self.debugTimer = wpilib.Timer()
        self.debugTimer.start()

        states = []

        #debug print states
        #keep them here in case you just want a timer and print statements
        
        # idle
        # lower
        # standby
        # intake
        # eject
        # raise
        # wait
        # handoff

        #print versions
        # idle = State(
        #     name="Idle",
        #     transition=lambda: "Lower" if random.random() < CHANCE_TO_SIGHT else "",
        #     exit=lambda: print("Exited")
        # )
        # states.append(idle)

        # #lower intake for prep
        # lower = State(
        #     name="Lower",
        #     enter=lambda: self.debugTimer.reset(),
        #     transition=lambda: "Standby" if self.debugTimer.advanceIfElapsed(LOWER_TIME) else ""
        # )
        # states.append(lower)

        # #wait until properly aligned
        # standby = State(
        #     name="Standby",
        #     transition=lambda: "Intake" if self.debugTimer.advanceIfElapsed(STANDBY_TIME) else ""
        # )
        # states.append(standby)

        # #try to intake note
        # intake = State(
        #     name="Intake",
        #     transition=lambda: "Eject" if random.random() < CHANCE_TO_JAM else "Raise"
        # )
        # states.append(intake)

        # #eject if something is wrong
        # eject = State(
        #     name="Eject",
        #     enter=lambda: self.debugTimer.reset(),
        #     transition=lambda: "Idle" if self.debugTimer.advanceIfElapsed(1) else ""
        # )
        # states.append(eject)

        # #raise to handoff position
        # #this is when the master machine would tell the shooter
        # raiseIntake = State(
        #     name="Raise",
        #     enter=lambda: self.debugTimer.reset(),
        #     transition=lambda: "Wait" if self.debugTimer.advanceIfElapsed(RAISE_TIME) else ""
        # )
        # states.append(raiseIntake)

        # wait = State(
        #     name="Wait",
        #     transition=lambda: "Handoff"
        # )
        # states.append(wait)

        # handoff = State(
        #     name="Handoff",
        #     enter=lambda: self.debugTimer.reset(),
        #     transition=lambda:"Idle" if self.debugTimer.advanceIfElapsed(1) else ""
        # )
        # states.append(handoff)
        
        # real version
        idle = State(
            name="Idle",
            transition=lambda: "Lower"
        )
        states.append(idle)

        #lower intake for prep
        lower = State(
            name="Lower",
            enter=lambda: getPivotInstantCommand(self.pivotController, lambda: self.pivotController.setGroundPickup()),
            transition=lambda: "Standby" if self.pivotController.isPivotPositioned() else ""
        )
        states.append(lower)

        #wait until properly aligned
        standby = State(
            name="Standby",
            transition=lambda: "Intake"
        )
        states.append(standby)

        #try to intake note
        intake = State(
            name="Intake",
            enter=lambda: self.debugTimer.reset(),
            run=lambda: self.intake.runIntake(0.4),
            transition=lambda: "Raise" if self.debugTimer.advanceIfElapsed(0.25) else "",
            exit=lambda: self.intake.runIntake(0),
            cannotInterupt=True
        )
        states.append(intake)
        
        #eject if something is wrong
        eject = State(
            name="Eject",
            enter=lambda: self.intake.runIntake(-0.4),
            transition=lambda: "Idle" if self.debugTimer.advanceIfElapsed(1) else "",
            exit=lambda: self.intake.runIntake(0),
            cannotInterupt=True
        )
        states.append(eject)

        #raise to handoff position
        #this is when the master machine would tell the shooter
        raiseIntake = State(
            name="Raise",
            enter=lambda: getPivotInstantCommand(self.pivotController, lambda: self.pivotController.setHandOffPickup()),
            transition=lambda: "Wait" if self.pivotController.isPivotPositioned() else ""
        )
        states.append(raiseIntake)

        wait = State(
            name="Wait",
            transition=lambda: "Handoff" if self.debugTimer.advanceIfElapsed(1) else ""
        )
        states.append(wait)

        handoff = State(
            name="Handoff",
            run=lambda: self.intake.runIntake(-0.4),
            exit=lambda: self.intake.runIntake(0),
            cannotInterupt=True
            #transition=lambda:"Idle" if self.debugTimer.advanceIfElapsed(0.5) else ""
        )
        states.append(handoff)
        
        super().__init__(states, None, debugMode)
    
    def enable(self):
        #custom behaviour to reset timer upon being re-enabled
        #should prob reset on disable but idc fix it yourself
        self.debugTimer.reset()
        return super().enable()