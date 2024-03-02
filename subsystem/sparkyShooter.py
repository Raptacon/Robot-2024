import commands2
import rev
import utils.sparkMaxUtils
import wpilib
class Shooter(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.intakeMotor = rev.CANSparkMax(23, rev.CANSparkLowLevel.MotorType.kBrushless)
        utils.sparkMaxUtils.configureSparkMaxCanRates(self.intakeMotor)
        self.intakeMotor.setInverted(True)
        self.leftShootMotor = rev.CANSparkMax(24, rev.CANSparkLowLevel.MotorType.kBrushless)
        utils.sparkMaxUtils.configureSparkMaxCanRates(self.leftShootMotor)
        self.rightShooterMotor = rev.CANSparkMax(25, rev.CANSparkLowLevel.MotorType.kBrushless)
        utils.sparkMaxUtils.configureSparkMaxCanRates(self.rightShooterMotor)
        self.rightShooterMotor.setInverted(False)

        self.leftShootMotor.enableVoltageCompensation(12)
        self.rightShooterMotor.enableVoltageCompensation(12)
        self.leftEncoder = self.leftShootMotor.getEncoder()
        self.rightEncoder = self.rightShooterMotor.getEncoder()

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("left shooter speed", self.leftEncoder.getVelocity())
        wpilib.SmartDashboard.putNumber("right shooter speed", self.rightEncoder.getVelocity())

    def runIntake(self, speed : float):
        self.intakeMotor.set(speed)

    def runShooters(self, voltage : float):
        self.leftShootMotor.setVoltage(voltage)
        self.rightShooterMotor.setVoltage(voltage)
