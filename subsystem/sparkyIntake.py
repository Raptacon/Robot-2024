import commands2
import rev

class SparkyIntake(commands2.SubsystemBase):
    def __init__(self) -> None:
        self.intakeMotor = rev.CANSparkMax(21, rev.CANSparkLowLevel.MotorType.kBrushless)

    def runIntake(self, percent : float):
        speed = max(-0.5, min(percent, 0.5))
        self.intakeMotor.set(percent)
