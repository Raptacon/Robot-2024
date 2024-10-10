import commands2
import commands2.cmd
from commands.autoDrive import AutoDrive
from subsystem.swerveDriveTrain import Drivetrain
from commands.sparkyAuto import HandOff
from subsystem.sparkyShooter import Shooter
from subsystem.sparkyIntake import SparkyIntake
from commands.autoSparkyShooterPivot import AutoShooterPivot
from subsystem.sparkyShooterPivot import ShooterPivot
from subsystem.sparkyIntakePivotController import getPivotInstantCommand, pivotController
import logging

log = logging.getLogger("Auto")

class SparkyShoot(commands2.SequentialCommandGroup):
    def __init__(self, shooter : Shooter, intake : SparkyIntake, drive: Drivetrain, intakePivot : pivotController, shooterPivot : ShooterPivot) -> None:
        super().__init__()
        self.addCommands(
            AutoShooterPivot(shooterPivot, "loading"),
            getPivotInstantCommand(intakePivot, intakePivot.setGroundPickup),
        )
