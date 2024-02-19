import commands2
import commands2.cmd
from commands.goToDist import GoToDist
from subsystem.swerveDriveTrain import Drivetrain
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

