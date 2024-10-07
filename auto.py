import commands2
import commands2.cmd
from commands.autoDrive import AutoDrive
from subsystem.swerveDriveTrain import Drivetrain
from commands.sparkyAuto import HandOff
from subsystem.sparkyShooter import Shooter
from subsystem.sparkyIntake import SparkyIntake
import logging

log = logging.getLogger("Auto")

class SparkyShoot(commands2.SequentialCommandGroup):
    def __init__(self, shooter : Shooter, intake : SparkyIntake, drive: Drivetrain) -> None:
        super().__init__()
        self.addCommands(
            commands2.PrintCommand("Running Shooter"),
            HandOff(shooter, intake, 2, 0.4),
            commands2.PrintCommand("Finished Shooter"),
            AutoDrive(.01, 0, -.1, 0.2, True, drive), #align wheels
            AutoDrive(1.0, 0, 0.0, 0.0, True, drive), #safe the drive train until we are stable
            commands2.PrintCommand("AutoDrive Align finished"),
            AutoDrive(1.2, 0, -0.2, 0.0, True, drive), #drive forward about 6 ft, arm going down during this
            commands2.PrintCommand("AutoDrive first move finished"),
            AutoDrive(0.2, 0, -0.2, 0, True, drive), #drive foward about 1 ft, may need to change values, arm sucking peice
            commands2.PrintCommand("AutoDrive second move finished"),
            AutoDrive(1.4, 0, 0.2, 0, True, drive), #move back to the scoring area, may need to change values, arm going up during this
            commands2.PrintCommand("AutoDrive final move finnished"),
        )
