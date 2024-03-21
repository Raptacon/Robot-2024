import commands2
from subsystem.sparkyShooter import Shooter
import wpilib

class SparkyFeeder(commands2.Command):
    def __init__(self, delay : float, timeS : float, speed : float, shooterSpeed : float, shooter : Shooter):
        self.timeS = timeS
        self.delay = delay
        self.speed = speed
        self.shooterSpeed = shooterSpeed
        self.shooter = shooter
        self.finishedDelay = False
        self.addRequirements(shooter)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        self.timer = wpilib.Timer()
        self.timer.start()

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        if(self.timer.hasElapsed(self.delay) and not self.finishedDelay):
            self.timer.reset()
            self.finishedDelay = True
        if(self.timer.hasElapsed(self.delay) or self.finishedDelay):
            self.shooter.runIntake(self.speed)
            self.shooter.runShooters(-self.shooterSpeed)

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        self.shooter.runIntake(0)

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        # Compare distance travelled from start to desired distance
        return self.timer.hasElapsed(self.timeS)
