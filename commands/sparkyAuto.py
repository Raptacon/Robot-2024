import commands2
from subsystem.sparkyIntake import SparkyIntake
from subsystem.sparkyShooter import Shooter
import time
from subsystem.swerveDriveTrain import Drivetrain
import wpimath.controller
from wpimath.geometry import Pose2d, Transform2d
import wpimath.units
import math

class HandOff(commands2.CommandBase):
    def __init__(self, shooter : Shooter, intake : SparkyIntake, maxTime : float, shooterWait : float) -> None:
        super().__init__()
        self.shooter = shooter
        self.intake = intake
        self.shooterWait = shooterWait
        self.maxTime = maxTime

    def initialize(self) -> None:
        self.startingTime = time.time()

    def execute(self) -> None:
        self.currentTime = time.time() - self.startingTime
        self.shooter.runShooters(1)
        if(self.currentTime >= self.shooterWait):
            self.intake.runIntake(-0.4)
            self.shooter.runIntake(0.4)
    
    def isFinished(self) -> bool:
        return self.currentTime >= self.maxTime
    
    def end(self, interrupted: bool) -> None:
        self.intake.runIntake(0)
        self.shooter.runIntake(0)
        self.shooter.runShooters(0)

class GoForTime(commands2.CommandBase):
    def __init__(self, maxTime : float, drive : Drivetrain) -> None:
        """Creates a new DriveDistance. This command will drive your your robot for a set period of time, should drive forward on the robots Y axis."""
        super().__init__()
        self.maxTime = maxTime
        self.drive = drive
        self.addRequirements(drive)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        print("Init drive2distance")
        self.drive.drive(0, 0, 0, True)
        self.drive.resetHeading()
        self.startingTime = time.time()

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.currentTime = time.time() - self.startingTime
        self.drive.drive(0, 0.5, 0 ,True)

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        self.drive.resetHeading()
        self.drive.drive(0, 0, 0, True)

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        # Compare distance travelled from start to desired distance
        return self.currentTime >= self.maxTime

class GoToPos(commands2.PIDSubsystem):
    targetPos = Pose2d()
    tolerance = Transform2d(0.5, 0.5, 0.1)
    def __init__(self, targetPos: Pose2d, drive: Drivetrain) -> None:
        """Creates a new DriveDistance. This command will drive your your robot to a designated cordinate.
        targetPos: The X and Y pos that the bot will drive to(in meters)
        drive:  The drivetrain subsystem on which this command will run
        """
        self.targetPos = targetPos
        self.drive = drive
        self.pid = wpimath.controller.PIDController(0.1, 0.0, 0.0)
        self.pid.setTolerance(0.1, 0.1)
        super().__init__(self.pid)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        print("Init drive2distance")
        self.drive.drive(0, 0, 0, True)
        self.pid.reset()
        self.drive.resetHeading()
        self.startingPos = self.drive.getPos()

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        if(not self.drive.getPos()): return
        self.dist = self.drive.getPos() - self.startingPos

        self.totalOffset = self.targetPos - self.dist

        self.speedX = self.pid.calculate(self.dist.X(), self.targetPos.X())
        self.speedY = self.pid.calculate(self.dist.Y(), self.targetPos.Y())

        print(f"pos : {self.drive.getPos().Y()} offsetX : {self.totalOffset.X()} offsetY : {self.totalOffset.Y()}")

        self.drive.drive(self.speedX, self.speedY, 0 ,True)

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        self.drive.drive(0, 0, 0, True)
        self.drive.resetHeading()
        self.pid.reset()

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        # Compare distance travelled from start to desired distance
        return self.totalOffset < self.tolerance
