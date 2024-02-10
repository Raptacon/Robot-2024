import commands2
import rev


class SwerveIntakePivot(commands2.SubsystemBase):
    def __init__(self) -> None:
        self.pivotMotor = rev.CANSparkMax(22, rev.CANSparkLowLevel.MotorType.kBrushless)

    def runPivot(self, percent : float):
        self.pivotMotor.set(percent)