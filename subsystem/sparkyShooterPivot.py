import commands2
import rev
import wpilib
import wpimath
import wpimath.controller
import utils.sparkMaxUtils
class ShooterPivot(commands2.PIDSubsystem):
    normalPid = {"Kp": 72, "Ki": 0, "Kd": 0}
    climbPid = {"Kp": 72*4, "Ki": 0, "Kd": 0}
    kClimbCurrent = 50
    kNormalCurrent = 20
    def __init__(self) -> None:
        pidController = wpimath.controller.PIDController(**self.normalPid)
        pidController.setTolerance(0.1)
        super().__init__(pidController, 0)

        self.pivotMotorRight = rev.CANSparkMax(31, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.pivotMotorLeft = rev.CANSparkMax(26, rev.CANSparkLowLevel.MotorType.kBrushless)
        utils.sparkMaxUtils.configureSparkMaxCanRates(self.pivotMotorRight)
        self.pivotMotorRight.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.pivotMotorRight.setInverted(False)

        self.pivotMotorLeft.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.pivotMotorLeft.setInverted(True)

        self.encoderRight = self.pivotMotorRight.getEncoder()
        self.encoderLeft = self.pivotMotorLeft.getEncoder()
        #scaled to 0..1 = forward - end limit
        #80:1 use 1/73.38 100:1 use 88.056
        self.encoderRight.setPositionConversionFactor(1/88.056)
        self.encoderRight.setPosition(0)
        self.encoderLeft.setPositionConversionFactor(1/88.056)
        self.encoderLeft.setPosition(0)

        # Enable softlimit for negative direction. Note that all postions go from 0..~ -1
        self.pivotMotorRight.enableSoftLimit(rev.CANSparkMax.SoftLimitDirection.kReverse, True)
        self.pivotMotorRight.setSoftLimit(rev.CANSparkMax.SoftLimitDirection.kReverse, -1.0)
        self.pivotMotorLeft.enableSoftLimit(rev.CANSparkMax.SoftLimitDirection.kReverse, True)
        self.pivotMotorLeft.setSoftLimit(rev.CANSparkMax.SoftLimitDirection.kReverse, -1.0)

        #get limits
        self.forwardLimit = self.pivotMotorRight.getForwardLimitSwitch(rev.SparkMaxLimitSwitch.Type.kNormallyClosed)
        self.reverseLimit = self.pivotMotorRight.getReverseLimitSwitch(rev.SparkMaxLimitSwitch.Type.kNormallyClosed)

        self.motorFeedforward = wpimath.controller.SimpleMotorFeedforwardMeters(0, 0, 0)
        self.motorCurrent = None
        self.setMotorCurrent(self.kNormalCurrent)

        #setup default values
        self.zeroed = False
        self.zeroing = False
        self.coasting = False

    def runPivot(self, speed : float):
        self.setMotor(speed)


    def getMeasurement(self):
        return -self.encoderRight.getPosition()

    def setPostion(self, position: float):
        return

    def periodic(self):
        super().periodic()
        if wpilib.DriverStation.isEnabled() and self.coasting:
            self.coasting = False
            self.pivotMotorRight.setIdleMode(rev.CANSparkBase.IdleMode.kBrake)
            self.pivotMotorLeft.setIdleMode(rev.CANSparkBase.IdleMode.kBrake)

        elif not self.coasting:
            self.coasting = True
            #self.pivotMotorRight.setIdleMode(rev.CANSparkBase.IdleMode.kCoast)
            #self.pivotMotorLeft.setIdleMode(rev.CANSparkBase.IdleMode.kCoast)

        wpilib.SmartDashboard.putNumber("Left Climb Current", self.pivotMotorLeft.getOutputCurrent())
        wpilib.SmartDashboard.putNumber("Right Climb Current", self.pivotMotorRight.getOutputCurrent())
        
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
        wpilib.SmartDashboard.putNumber("Shooter Pos Current", self.pivotMotorRight.getOutputCurrent())

        self.voltage = output + feedforward
        wpilib.SmartDashboard.putNumber("Shooter Pos voltage", self.voltage)
        self.voltage = max(-10, min(self.voltage, 10))
        #print(f"using output {output} {setpoint} {self.voltage}")
        self.pivotMotorRight.setVoltage(-self.voltage)
        self.pivotMotorLeft.setVoltage(-self.voltage)
        wpilib.SmartDashboard.putNumber("Shooter pos", self.encoderRight.getPosition())

    def zeroPivot(self, speed : float = 0.2):
        self.zeroing = True
        if not self.forwardLimit.get():
            #disable limit to allow zeroing
            self.pivotMotorRight.enableSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, False)
            self.pivotMotorLeft.enableSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, False)

            self.zeroed = False
            self.setMotor(speed)
            return False
        else:
            self.zeroing = False
            self.zeroed = True
            self.setMotor(0.0)
            self.encoderRight.setPosition(0)
            self.encoderLeft.setPosition(0)
            #once zeroed, set softlimit to allow a soft "landing"
            self.pivotMotorRight.enableSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, True)
            self.pivotMotorLeft.enableSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, True)
            self.setSoftLimitForward(-0.01)

            return True

    def maxPivot(self, speed : float = 0.2):
        wpilib.SmartDashboard.putNumber("Shooter pos", self.encoderRight.getPosition())

        if not self.reverseLimit.get():
            self.setMotor(-speed)
            return False
        else:
            self.setMotor(0.0)
            return True

    #sets loading angle
    def setLoading(self):
        if not self.isEnabled():
            #allow for other modes to adjust PID
            self.getController().setPID(**self.normalPid)
            self.setSoftLimitForward(0.00)

        self.enable()
        self.setMotorCurrent(self.kNormalCurrent)
        self.setSetpoint(0)

    #sets amp angle
    def setAmp(self):
        if not self.isEnabled():
            #allow for other modes to adjust PID
            self.getController().setPID(**self.normalPid)
            self.setSoftLimitForward(0.0)

        self.enable()
        self.setMotorCurrent(self.kNormalCurrent)

        self.setSetpoint(0.4)

    def setClimb(self):
        #norminal goal is 0.05 for climbing postion
        if self.getMeasurement() < 0.008 and not self.isEnabled():
            #TODO add function to turn off when close enough
            print("limited")
        elif self.isEnabled():
            #climbing we need increased current, we will not use PID since we need a strong quick pull
            # and a soft limit will be used to disable output
            self.disable()
            if self.setMotorCurrent(self.kNormalCurrent):
                return

        self.runPivot(0.4)


    def setMotor(self, percent: float):
        self.pivotMotorLeft.set(percent)
        self.pivotMotorRight.set(percent)

    def setSoftLimitForward(self, limit: float):
        self.pivotMotorRight.setSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, 0.00)
        self.pivotMotorLeft.setSoftLimit(rev.CANSparkMax.SoftLimitDirection.kForward, 0.00)

    def setMotorCurrent(self, current: int):
        #set to override to one current limit
        #current = int(50.0)
        current = int(current)
        if(self.motorCurrent == current):
            return False

        wpilib.SmartDashboard.putNumber("Shoot Pivot Current", current)
        self.motorCurrent = current

        self.pivotMotorLeft.setSmartCurrentLimit(current)
        self.pivotMotorRight.setSmartCurrentLimit(current)
        return True

