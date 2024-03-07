from stateMachines.stateMachine import *
import wpilib

#FOR REFERENCE
#stateMachines\testIntakeDiagram.md
class TestIntakeStateMachine(StateMachine):
    #don't need to include all args because this state machine is predefined in its states/init state
    def __init__(self, debugMode=False, intake=None, pivot=None):
        #init some variables
        self.intake = intake
        self.pivot = pivot

        self.debugTimer = wpilib.Timer()

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

        lowerIntake = State(
            name="LowerIntake",
            enter=lambda: self.debugTimer.start(),
            transition=lambda: "SpinIntakeMotor" if self.debugTimer.advanceIfElapsed(4) else ""
        )
        states.append(lowerIntake)
        
        spinIntakeMotor = State(    
            name="SpinIntakeMotor",
            run=lambda: print("Spinning"),
            transition=lambda: "RaiseIntake" if self.debugTimer.advanceIfElapsed(0.5) else ""
        )
        states.append(spinIntakeMotor)
        
        raiseIntake = State(
            name="RaiseIntake",
            transition=lambda: "DoneState" if self.debugTimer.advanceIfElapsed(3) else ""
        )
        states.append(raiseIntake)

        doneState = State(name="DoneState")
        states.append(doneState)

        super().__init__(states, None, debugMode)
    
    def enable(self):
        #custom behaviour to reset timer upon being re-enabled
        #should prob reset on disable but idc fix it yourself
        self.debugTimer.reset()
        return super().enable()