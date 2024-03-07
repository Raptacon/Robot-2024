from stateMachines.testIntake import *
from stateMachines.testShooter import *

class UltraStateMachine(StateMachine):
    def __init__(self, states=[], initialState=None, debugMode=False):
        self.intakeSM = TestIntakeStateMachine(debugMode=debugMode)
        self.shooterSM = TestShooterStateMachine(debugMode=debugMode)

        self.intakeSM.enable()
        self.shooterSM.enable()

        states = []
        
        run = State(
            name="Run",
            run=lambda: self.runMachines(),
            transition=lambda: ""
        )
        states.append(run)
        
        handshake = State(
            name="Handshake",
            enter=lambda: self.organizeHandshake(),
            run=lambda: self.runHandshake()
        )
        states.append(handshake)

        super().__init__(states, initialState, debugMode)
    
    def runMachines(self):
        self.intakeSM.run()
        self.shooterSM.run()

        if str(self.intakeSM.state) == "DoneState":
            self.setState("Handshake")
    
    def runHandshake(self):
        self.shooterSM.run()
        self.shooterSM.overrideState("OtherTest")
    
    def organizeHandshake(self):
        self.shooterSM.setState("Test")
