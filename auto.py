import commands2
import commands2.cmd
from commands.goToDist import GoToDist
from subsystem.swerveDriveTrain import Drivetrain
from commands.sparkyAuto import HandOff
from subsystem.sparkyShooter import Shooter
from subsystem.sparkyIntake import SparkyIntake
import logging
from wpimath.geometry import Pose2d

log = logging.getLogger("Auto")
class Autonomous(commands2.SequentialCommandGroup):
    def __init__(self, drive : Drivetrain) -> None:
        super().__init__()
        self.addCommands(
            commands2.PrintCommand(f"GoToDist started"),
            GoToDist(Pose2d(0, 2, 0), drive),
            commands2.PrintCommand(f"GoToDist finished")
        )

class SparkyShoot(commands2.SequentialCommandGroup):
    def __init__(self, shooter : Shooter, intake : SparkyIntake, drive : Drivetrain) -> None:
        super().__init__()
        self.addCommands(
            commands2.PrintCommand("Running Shooter"),
            HandOff(shooter, intake, 3, 1),
            commands2.PrintCommand("Finished Shooter"),
        )
