from stateMachines.stateMachine import *
import wpilib

#stateMachines\testIntakeDiagram.md
class TestIntakeStateMachine(StateMachine):
    def __init__(self, states=[], initialState=None, debugMode=False, intake=None):
        
        # if intake == None:
        #     raise Exception("Must include intake in intake state machine!")
        
        # self.intake = intake

        self.debugTimer = wpilib.Timer()
        self.debugTimer.start()

        states = []

        # lowerIntake = State(
        #     name="LowerIntake",
        #     run=lambda: self.intake.setGroundPickup(),
        #     transition=lambda: "SpinIntakeMotor" if self.intake.isAtSetpoint() else ""
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
        #     transition=lambda: "DoneState" if self.intake.isAtSetpoint() else ""
        # )
        # states.append(raiseIntake)

        # doneState = State(
        #     name="DoneState"
        # )
        # states.append(doneState)

        lowerIntake = State(
            name="LowerIntake",
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

        super().__init__(states, initialState, debugMode)
    
    def enable(self):
        self.debugTimer.reset()
        return super().enable()