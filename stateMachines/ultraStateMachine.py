from stateMachines.testIntake import *
from stateMachines.testShooter import *

class UltraStateMachine(StateMachine):
    def __init__(self, debugMode=False):
        self.intakeSM = TestIntakeStateMachine(debugMode=debugMode)
        self.shooterSM = TestShooterStateMachine(debugMode=debugMode)

        self.intakeSM.enable()
        self.shooterSM.enable()

        self.preppingForHandoff = False

        states = []
        
        #run machines as normal
        run = State(
            name="Run",
            run=lambda: self.runMachines(),
            transition=lambda: ""
        )
        states.append(run)
        
        #force both machines to begin handoff prep
        prepHandoff = State(
            name="PrepHandoff",
            run=lambda: self.attemptPrepHandoff(),
            transition=lambda: "Handoff" if (str(self.intakeSM.state) == "Wait" and str(self.shooterSM.state) == "Wait") else "" #possibly should add edge case for if certain time elapses
        )
        states.append(prepHandoff)

        #This goes off for one tick and simply changes the state machines to handoff mode.
        #At this point, the master machine shouldn't care what happens
        handoff = State(
            name="Handoff",
            enter=lambda: self.runHandoff(),
            transition=lambda: "Run"
        )
        states.append(handoff)

        super().__init__(states, None, debugMode)
    
    def run(self) -> bool:
        #master machine ALWAYS runs these two machines
        self.intakeSM.run()
        self.shooterSM.run()

        print(f"{self.intakeSM.state} | {self.shooterSM.state}")
        return super().run()
    
    #standard run
    #check for intake machine being in the raise state to prep handoff
    def runMachines(self):
        if str(self.intakeSM.state) == "Wait" and str(self.shooterSM.state) == "Standby":
            self.overrideState("PrepHandoff")
    
    def attemptPrepHandoff(self):
        #keep trying to go to lower until shooter is ready
        if not self.preppingForHandoff:
            self.shooterSM.overrideState("Lower")
            self.preppingForHandoff = True
    
    def runHandoff(self):
        self.intakeSM.overrideState("Handoff")
        self.shooterSM.overrideState("Handoff")