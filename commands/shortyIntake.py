import commands2
import typing
from subsystem.sparkyIntake import SparkyIntake
from subsystem.sparkyIntakePivotController import pivotController
from utils.breakBeamFactory import createBreakBeam
import wpilib

class Intake(commands2.CommandBase):
    def __init__(self, intake: SparkyIntake, pivot : pivotController, intakePercent: typing.Callable[[], float], spitOut: typing.Callable[[], bool], changePivot : typing.Callable[[], bool], controllers : list[wpilib.XboxController]) -> None:
        super().__init__()
        self.intake = intake
        self.pivot = pivot
        self.intakePercent = intakePercent
        self.spitOut = spitOut

        self.rotatePivot = False
        self.changePivot = changePivot
        self.beam = None
        self.previousBeam = False

        self.controllers = controllers
        self.timer = wpilib.Timer()

        self.addRequirements(self.intake, self.pivot)

    def execute(self):
        if(self.spitOut()):
            self.intake.runIntake(-0.2)
        else:
            self.intake.runIntake(self.intakePercent())

        if(self.changePivot()):
            self.rotatePivot = not self.rotatePivot
            
        if(self.rotatePivot):
            self.pivot.setGroundPickup()
        else:
            self.pivot.setHandOffPickup()


        print(self.checkBeamBrake())
        if(self.checkBeamBrake() and not self.previousBeam):
            self.timer.start()

        if(not self.timer.hasElapsed(1)):
            self.sendPulse(0.5)
        else:
            self.timer.reset()
            self.sendPulse(0)
            
        self.previousBeam = self.checkBeamBrake()

    def checkBeamBrake(self) -> bool:
        if(not self.beam):
            self.beam = createBreakBeam(1)
            return False

        return self.beam.get()
    
    def sendPulse(self, power : float):
        for controller in self.controllers:
            controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, power)
