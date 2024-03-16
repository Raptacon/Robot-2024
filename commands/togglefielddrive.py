import commands2
import typing
from subsystem.swerveDriveTrain import Drivetrain

class ToggleFieldDrive(commands2.InstantCommand):
    def __init__(self, 
                 driveTrain: Drivetrain, 
                 robotRelative: typing.Callable[[],bool]) -> None:
        super().__init__()
        self.driveTrain = driveTrain
        self.robotRelative = robotRelative
        self.addRequirements(driveTrain)

    def execute(self) -> None:
        print(f"Toggling field relative from {self.driveTrain.getFieldDriveRelative()} to {not self.robotRelative()}")
        self.driveTrain.setFieldDriveRelative(not self.robotRelative())

