import commands2
import commands2.cmd
import wpimath.controller
from subsystem.swerveDriveTrain import Drivetrain
from wpimath.geometry import Pose2d, Transform2d
import wpimath.units

class GoToDist(commands2.CommandBase):
    targetPos = Pose2d()
    tolerance = Transform2d(0.5, 0.5, 0)
    def __init__(self, targetPos: Pose2d, drive: Drivetrain) -> None:
        """Creates a new DriveDistance. This command will drive your your robot to a designated cordinate.
        targetPos: The X and Y pos that the bot will drive to(in meters)
        drive:  The drivetrain subsystem on which this command will run
        """
        super().__init__()
        self.targetPos = targetPos
        self.drive = drive
        self.pid = wpimath.controller.PIDController(0.01, 0.0, 0.0)
        self.pid.setTolerance(0.5, 0.5)
        self.addRequirements(drive)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        print("Init drive2distance")
        #self.drive.drive(0, 0, 0, True)
        self.pid.reset()
        self.drive.resetHeading()
        self.startingXDistance = abs(self.drive.getPos().X() - self.targetPos.X())
        self.startingYDistance = abs(self.drive.getPos().Y() - self.targetPos.Y())

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        if(not self.drive.getPos()): return
        self.distX = self.drive.posX - self.startingXDistance
        self.distY = self.drive.posY - self.startingYDistance

        self.totalOffsetY = self.targetPos.Y() - self.distY
        self.totalOffsetX = self.targetPos.X() - self.distX

        self.drive.updateOdometry()

        self.speedX = self.pid.calculate(self.targetPos.X(), self.distX)
        self.speedY = self.pid.calculate(self.targetPos.Y(), self.distY)

        print(f"pos : {self.drive.getPos().Y()} offset : {self.totalOffsetY}")

        #self.drive.drive(0, 0, 0 ,True)

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        #self.drive.drive(0, 0, 0, True)
        self.drive.resetHeading()
        self.pid.reset()

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        # Compare distance travelled from start to desired distance
        return self.totalOffsetY < self.tolerance.Y() and self.totalOffsetX < self.tolerance.X()
