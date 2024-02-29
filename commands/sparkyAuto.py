import commands2
from subsystem.sparkyIntake import SparkyIntake
from subsystem.sparkyShooter import Shooter
import time

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
