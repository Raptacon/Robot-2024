import commands2
import wpilib.event
from subsystem.sparkyShooter import Shooter
from subsystem.sparkyShooterPivot import ShooterPivot
import typing
import math
from commands.sparkyFeeder import SparkyFeeder

class ShooterCommand(commands2.CommandBase):
    def __init__(self,
                 shooter : Shooter,
                 pivot: ShooterPivot,
                 intaking : typing.Callable[[], bool],
                 outaking : typing.Callable[[], bool],
                 shooterSpeed : typing.Callable[[], float],
                 pivotToggle: typing.Callable[[], bool],
                 ferryPos : typing.Callable[[], bool],
                 manualPivotControl : typing.Callable[[], bool],
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

        self.manualPivotControl = manualPivotControl
        self.manualInput = manualInput
        self.manualPivot = False

        self.climbing = False

        self.ferryPos = ferryPos
        self.ferrying = False

        self.addRequirements(self.shooter, self.pivot)

    def execute(self):
        if(self.intaking()):
            self.shooter.runIntake(0.1)
        elif(self.outaking()):
            self.shooter.runIntake(-0.1)
        else:
            self.shooter.runIntake(0)

        voltage = 0
        # set full speed if enabling shooter
        if self.shooterSpeed() > 0.2:
            voltage = 12.0
        self.shooter.runShooters(voltage)

        #priority
        # Manual
        # cancle manual
        # climbing
        # cancle climbing
        # pos toggle
        if(self.manualPivotControl()): #manual
            self.manualPivot = True
            self.pivot.disable()
            self.pivot.setMotorCurrent(self.pivot.kClimbCurrent)
            #square the inputs to allow agradual add on.
            self.pivot.runPivot(math.copysign(1.0, self.manualInput())*self.manualInput()**2)
        elif self.manualPivot: #cancle Manual
            self.pivot.runPivot(0)
            self.pivot.setMotorCurrent(self.pivot.kNormalCurrent)
            self.manualPivot = False
        elif self.climbing: # climbing canceled
            #disable on button release
            self.climbing = False
            self.pivot.setMotor(0)
        elif self.ferryPos():
            self.pivot.setFerry()
            self.ferry = SparkyFeeder(0.1, 0.1, -0.15, 2, self.shooter)
            self.ferry.schedule()
        elif self.pivotToggle(): #toggling piviot
            #enable PID incase we disabled in another mode
            self.pivot.enable()
            if self.pivotLoad:
                self.pivotLoad = False
                self.pivot.setAmp()
            else:
                self.pivotLoad = True
                self.pivot.setLoading()
