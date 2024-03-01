import commands2
from subsystem.sparkyShooter import Shooter
from subsystem.sparkyShooterPivot import ShooterPivot
import typing

class ShooterCommand(commands2.CommandBase):
    def __init__(self,
                 shooter : Shooter,
                 pivot: ShooterPivot,
                 intaking : typing.Callable[[], bool],
                 outaking : typing.Callable[[], bool],
                 shooterSpeed : typing.Callable[[], float],
                 pivotToggle: typing.Callable[[], bool],
                 climbPos : typing.Callable[[], bool],
                 manualPiviotControl : typing.Callable[[], bool],
                 manualInput : typing.Callable[[], float]):
        super().__init__()

        self.shooter = shooter
        self.intaking = intaking
        self.outaking = outaking
        self.shooterSpeed = shooterSpeed
        self.pivotToggle = pivotToggle

        self.pivot = pivot
        self.pivotLoad = True
        self.pivot.enable()

        self.climbPos = climbPos

        self.manualPiviotControl = manualPiviotControl
        self.manualInput = manualInput
        self.manualPivot = False

        self.climbing = False

        self.addRequirements(self.shooter, self.pivot)

    def execute(self):
        if(self.intaking()):
            self.shooter.runIntake(0.2)
        elif(self.outaking()):
            self.shooter.runIntake(-0.2)
        else:
            self.shooter.runIntake(0)

        voltage = 0
        # set full speed if enabling shooter
        if self.shooterSpeed() > 0.2:
            voltage = 12.0
        self.shooter.runShooters(voltage)

<<<<<<< Updated upstream
        if(self.manualControl()):
            self.manualPivot = True
            self.pivot.disable()
            self.pivot.runPivot(self.manualInput())
        elif(self.manualControl() and self.manualPivot):
            self.pivot.runPivot(0)
            self.manualPivot = False

        if(self.pivotToggle()):
=======
        #priority
        # Manual
        # cancle manual
        # climbing
        # cancle climbing
        # pos toggle
        if(self.manualPiviotControl()): #manual
            self.manualPivot = True
            self.pivot.disable()
            self.pivot.runPivot(self.manualInput())
        elif self.manualPivot: #cancle Manual
            self.pivot.runPivot(0)
            self.manualPivot = False
        elif self.climbPos(): # climbing enabled
            self.climbing = True
            self.pivot.enable()
            self.pivot.setClimb()
        elif self.climbing: # climbing cancled
            #disable on button release
            self.climbing = False
            self.pivot.pivotMotor.set(0)
        elif self.pivotToggle(): #toggling piviot
>>>>>>> Stashed changes
            self.pivot.enable()
            if self.pivotLoad:
                self.pivotLoad = False
                self.pivot.setAmp()
            else:
                self.pivotLoad = True
                self.pivot.setLoading()
