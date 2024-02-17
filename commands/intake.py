import commands2
import typing
import rev
from subsystem.swerveIntake import SwerveIntake
from subsystem.swerveIntakePivot import SwerveIntakePivot

class Intake(commands2.CommandBase):
    def __init__(self, intake: SwerveIntake, pivot : SwerveIntakePivot, intakePercent: typing.Callable[[], float], spitOut: typing.Callable[[], bool], pivotPercent: typing.Callable[[], float]) -> None:
        super().__init__()
        self.intake = intake
        self.pivot = pivot
        self.intakePercent = intakePercent
        self.spitOut = spitOut
        self.pivotPercent = pivotPercent


        self.addRequirements(self.intake, self.pivot)

    def execute(self):
        if(self.spitOut()):
            self.intake.runIntake(-0.5)
        else:
            self.intake.runIntake(self.intakePercent())

        self.pivot.runPivot(self.pivotPercent())
        