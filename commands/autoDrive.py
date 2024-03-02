import commands2
import commands2.cmd
import wpilib
import wpimath.controller
from subsystem.swerveDriveTrain import Drivetrain
from wpimath.geometry import Pose2d, Transform2d

class AutoDrive(commands2.CommandBase):
    targetPos = Pose2d()
    tolerance = Transform2d(0.5, 0.5, 0)
    def __init__(self, timeS: float, speedX: float, speedY: float, dir: float, fieldRel: bool, drive: Drivetrain) -> None:
        """Creates a new DriveDistance. This command will drive your your robot to a designated cordinate.
        targetPos: The X and Y pos that the bot will drive to(in meters)
        drive:  The drivetrain subsystem on which this command will run
        """
        super().__init__()
        self.speedX = speedX
        self.speedY = speedY
        self.dir = dir
        self.drive = drive
        self.timeS = timeS
        self.fieldRel = fieldRel
        self.addRequirements(drive)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        self.drive.resetHeading()
        self.timer = wpilib.Timer()
        self.timer.start()
    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.drive.drive(self.speedX, self.speedY, self.dir, self.fieldRel)
        self.drive.updateOdometry()

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        self.drive.drive(0,0,0,False)

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        # Compare distance travelled from start to desired distance
        return self.timer.hasElapsed(self.timeS)
