import commands2
import rev
import wpilib
import wpimath
import wpimath.controller
import utils.sparkMaxUtils
class ShooterPivot(commands2.PIDSubsystem):
    def __init__(self) -> None:
        pidController = wpimath.controller.PIDController(72, 0, 0)
        pidController.setTolerance(0.1)
        super().__init__(pidController, 0)

        self.pivotMotor = rev.CANSparkMax(31, rev.CANSparkLowLevel.MotorType.kBrushless)
        utils.sparkMaxUtils.configureSparkMaxCanRates(self.pivotMotor)
        self.pivotMotor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.pivotMotor.setInverted(False)
        self.encoder = self.pivotMotor.getEncoder()
        #scaled to 0..1 = forward - end limit
        #80:1 use 1/73.38 100:1 use 88.056
        self.encoder.setPositionConversionFactor(1/88.056)

        #get limits
        self.forwardLimit = self.pivotMotor.getForwardLimitSwitch(rev.SparkMaxLimitSwitch.Type.kNormallyClosed)
        self.reverseLimit = self.pivotMotor.getReverseLimitSwitch(rev.SparkMaxLimitSwitch.Type.kNormallyClosed)

        self.motorFeedforward = wpimath.controller.SimpleMotorFeedforwardMeters(0, 0, 0)

        #setup default values
        self.zeroed = False
        self.zeroing = False

    def runPivot(self, speed : float):
        self.pivotMotor.set(speed)
        #wpilib.SmartDashboard.putNumber("Shooter pos", self.encoder.getPosition())

    def getMeasurement(self):
        return -self.encoder.getPosition()

    def setPostion(self, position: float):
        return

    def useOutput(self, output: float, setpoint: float):
        """
        if(self.manualControl): 
            self.controlManually()
            return
        
        if(self.maintainPosition):
            return
        """
        
        zeroing = self.zeroing
        #Do not use output until zeroed
        if not self.zeroed:
            #print("PID zeroing...")
            if not self.zeroPivot():
                return
        if zeroing:
            self.getController().reset()
            #print("Shooter angle controller reset")
            return

        feedforward = self.motorFeedforward.calculate(setpoint, 0)
        wpilib.SmartDashboard.putNumber("Shooter Pos Current", self.pivotMotor.getOutputCurrent())

        self.voltage = output + feedforward
        wpilib.SmartDashboard.putNumber("Shooter Pos voltage", self.voltage)
        self.voltage = max(-10, min(self.voltage, 10))
        #print(f"using output {output} {setpoint} {self.voltage}")
        self.pivotMotor.setVoltage(-self.voltage)
        wpilib.SmartDashboard.putNumber("Shooter pos", self.encoder.getPosition())

    def zeroPivot(self, speed : float = 0.2):
        self.zeroing = True
        if not self.forwardLimit.get():
            self.zeroed = False
            self.pivotMotor.set(speed)
            return False
        else:
            self.zeroing = False
            self.zeroed = True
            self.pivotMotor.set(0.0)
            self.encoder.setPosition(0)
            return True

    def maxPivot(self, speed : float = 0.2):
        wpilib.SmartDashboard.putNumber("Shooter pos", self.encoder.getPosition())
        
        if not self.reverseLimit.get():
            self.pivotMotor.set(-speed)
            return False
        else:
            #print(f"Done {self.getPosition()}")
            self.pivotMotor.set(0.0)
            wpilib.SmartDashboard.putNumber("Shooter pos", self.encoder.getPosition())
            return True

    #sets loading angle
    def setLoading(self):
        self.setSetpoint(0)

    #sets amp angle
    def setAmp(self):
        self.setSetpoint(0.4)

    def setClimb(self):
        self.setSetpoint(0.05)
