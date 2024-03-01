import commands2
import rev
import wpilib
import wpimath
import wpimath.controller
import utils.sparkMaxUtils
class ShooterPivot(commands2.PIDSubsystem):
    normalPid = {"Kp": 72, "Ki": 0, "Kd": 0}
    climbPid = {"Kp": 72*4, "Ki": 0, "Kd": 0}
    def __init__(self) -> None:
        pidController = wpimath.controller.PIDController(**self.normalPid)
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
        self.encoder.setPosition(0)
        
        # Enable softlimit for negative direction. Note that all postions go from 0..~ -1
        self.pivotMotor.enableSoftLimit(rev.CANSparkMax.SoftLimitDirection.kReverse, True)
        self.pivotMotor.setSoftLimit(rev.CANSparkMax.SoftLimitDirection.kReverse, -1.0)


        #get limits
        self.forwardLimit = self.pivotMotor.getForwardLimitSwitch(rev.SparkMaxLimitSwitch.Type.kNormallyClosed)
        self.reverseLimit = self.pivotMotor.getReverseLimitSwitch(rev.SparkMaxLimitSwitch.Type.kNormallyClosed)

        self.motorFeedforward = wpimath.controller.SimpleMotorFeedforwardMeters(0, 0, 0)

        #setup default values
        self.zeroed = False
        self.zeroing = False
        self.coasting = False

    def runPivot(self, speed : float):
        self.pivotMotor.set(speed)

    def getMeasurement(self):
        return -self.encoder.getPosition()

    def setPostion(self, position: float):
        return
    
    def periodic(self):
        super().periodic()
        if wpilib.DriverStation.isEnabled() and self.coasting:
            self.coasting = False
            self.pivotMotor.setIdleMode(rev.CANSparkBase.IdleMode.kBrake)
        elif not self.coasting:
            self.coasting = True
            self.pivotMotor.setIdleMode(rev.CANSparkBase.IdleMode.kCoast)
                

    def useOutput(self, output: float, setpoint: float):
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
            #disable limit to allow zeroing
            self.pivotMotor.enableSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, False)
            self.zeroed = False
            self.pivotMotor.set(speed)
            return False
        else:
            self.zeroing = False
            self.zeroed = True
            self.pivotMotor.set(0.0)
            self.encoder.setPosition(0)
            #once zeroed, set softlimit to allow a soft "landing"
            self.pivotMotor.setSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, -0.01)
            self.pivotMotor.enableSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, True)
            return True

    def maxPivot(self, speed : float = 0.2):
        wpilib.SmartDashboard.putNumber("Shooter pos", self.encoder.getPosition())
        
        if not self.reverseLimit.get():
            self.pivotMotor.set(-speed)
            return False
        else:
            self.pivotMotor.set(0.0)
            return True

    #sets loading angle
    def setLoading(self):
        if not self.isEnabled():
            #allow for other modes to adjust PID
            self.getController().setPID(**self.normalPid)
            self.pivotMotor.setSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, 0.00)

        self.enable()
        #self.pivotMotor.setSmartCurrentLimit(20)
        self.setSetpoint(0)

    #sets amp angle
    def setAmp(self):
        if not self.isEnabled():
            #allow for other modes to adjust PID
            self.getController().setPID(**self.normalPid)
            self.pivotMotor.setSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, 0.00)

        self.enable()
        #self.pivotMotor.setSmartCurrentLimit(20)
        self.setSetpoint(0.4)

    def setClimb(self):
        #norminal goal is 0.05 for climbing postion
        if self.getMeasurement() < 0.008 and not self.isEnabled():
            #TODO add function to turn off when close enough
            print("limited")
        elif self.isEnabled():
            #climbing we need increased current, we will not use PID since we need a strong quick pull
            # and a soft limit will be used to disable output
            #self.pivotMotor.setSmartCurrentLimit(60)
            self.disable()
            #self.pivotMotor.setSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, -0.045)
            #first round allow settings to update
            #return
        self.runPivot(0.8)
