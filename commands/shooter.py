import commands2
from subsystem.swerveShooter import SwerveShooter
from subsystem.swerveShooterPivotController import shooterPivotController
import typing

class Shooter(commands2.CommandBase):
    def __init__(self, shooter : SwerveShooter, intaking : typing.Callable[[], bool], outaking : typing.Callable[[], bool], shooterSpeed : typing.Callable[[], float], pivotController : shooterPivotController, changePivot : typing.Callable[[], bool]):
        super().__init__()

        self.shooter = shooter
        self.intaking = intaking
        self.outaking = outaking
        self.shooterSpeed = shooterSpeed

        self.pivotController = pivotController

        self.rotatePivot = False
        self.changePivot = changePivot

        self.addRequirements(self.shooter, self.pivotController)

    def execute(self):
        if(self.intaking()):
            self.shooter.runIntake(0.2)
        elif(self.outaking()):
            self.shooter.runIntake(-0.2)
        else:
            self.shooter.runIntake(0)

        if(self.changePivot()):
            self.rotatePivot = not self.rotatePivot

        self.shooter.runShooters(self.shooterSpeed())

        if(self.rotatePivot):
            self.pivotController.setAmpShoot()
        else:
            self.pivotController.setHandOffPickup()  
