import commands2
from subsystem.sparkyShooter import Shooter
from subsystem.sparkyShooterPivot import ShooterPivot
import typing

class ShooterCommand(commands2.CommandBase):
    def __init__(self,
                 shooter : Shooter,
                 pivot: ShooterPivot,
                 intaking : typing.Callable[[], bool],
                 outaking : typing.Callable[[], bool],
                 shooterSpeed : typing.Callable[[], float],
                 pivotToggle: typing.Callable[[], bool],
                 climbPos : typing.Callable[[], bool],
                 manualControl : typing.Callable[[], bool],
                 manualInput : typing.Callable[[], float]):
        super().__init__()

        self.shooter = shooter
        self.intaking = intaking
        self.outaking = outaking
        self.shooterSpeed = shooterSpeed
        self.pivotToggle = pivotToggle

        self.pivot = pivot
        self.pivotLoad = True
        self.pivot.enable()

        self.climbPos = climbPos

        self.manualControl = manualControl
        self.manualInput = manualInput

        self.addRequirements(self.shooter, self.pivot)

    def execute(self):
        if(self.intaking()):
            self.shooter.runIntake(0.2)
        elif(self.outaking()):
            self.shooter.runIntake(-0.2)
        else:
            self.shooter.runIntake(0)

        self.shooter.runShooters(self.shooterSpeed())

        self.pivot.checkManualControl(self.manualControl(), self.manualInput())

        if(self.pivotToggle()):
            if self.pivotLoad:
                self.pivotLoad = False
                self.pivot.setAmp()
            else:
                self.pivotLoad = True
                self.pivot.setLoading()

        if(self.climbPos()):
            self.pivot.setClimb()

