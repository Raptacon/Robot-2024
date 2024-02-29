import wpilib
import math

from subsystem.swerveDriveTrain import Drivetrain

from wpiutil.log import (
    DataLog, BooleanLogEntry, StringLogEntry, FloatLogEntry, IntegerLogEntry
)

telemetryButtonEntries = [
    ["AButton", BooleanLogEntry, "/button/letter/a"],
    ["BButton", BooleanLogEntry, "/button/letter/b"],
    ["XButton", BooleanLogEntry, "/button/letter/x"],
    ["YButton", BooleanLogEntry, "/button/letter/y"],
    ["BackButton", BooleanLogEntry, "/button/front/back"],
    ["StartButton", BooleanLogEntry, "/button/front/start"],
    ["LeftBumper", BooleanLogEntry, "/button/bumper/left"],
    ["RightBumper", BooleanLogEntry, "/button/bumper/right"],
    ["LeftStickButton", BooleanLogEntry, "button/stickbutton/left"],
    ["RightStickButton", BooleanLogEntry, "button/stickbutton/right"],
    ["RightTrigger", FloatLogEntry, "button/trigger/right"],
    ["LeftTrigger", FloatLogEntry, "button/trigger/left"],
    ["JoystickLeftY", FloatLogEntry, "button/joystick/lefty"],
    ["JoystickLeftX", FloatLogEntry, "button/joystick/leftx"],
    ["JoystickRightY", FloatLogEntry, "button/joystick/righty"],
    ["JoystickRightX", FloatLogEntry, "button/joystick/rightx"],
    ["DPad", IntegerLogEntry, "button/dpad"]
]

telemetryOdometryEntries = [
    ["xPositions", FloatLogEntry, "xpos"],
    ["yPositions", FloatLogEntry, "ypos"],
    ["angles", FloatLogEntry, "angle"]
]

telemetrySwerveDriveTrainEntries = []
for i in range(len(Drivetrain.kModuleProps)):
    telemetrySwerveDriveTrainEntries.extend([
        [f"steerDegree{i + 1}", FloatLogEntry, f"module{i + 1}/steerdegree"],
        [f"drivePercent{i + 1}", FloatLogEntry, f"module{i + 1}/drivepercent"],
        [f"moduleVelocity{i + 1}", FloatLogEntry, f"module{i + 1}/velocity"],
        [f"currSteerDegree{i + 1}", FloatLogEntry, f"module{i + 1}/currsteerdegree"]
    ])

driverStationEntries = [
    ["alliance", StringLogEntry, "alliance"],
    ["autonomous", BooleanLogEntry, "autonomous"],
    ["teleop", BooleanLogEntry, "teleop"],
    ["test", BooleanLogEntry, "test"],
    ["enabled", BooleanLogEntry, "enabled"]
]


class Telemetry:

    def __init__(
        self,
        driverController: wpilib.XboxController = None,
        mechController: wpilib.XboxController = None,
        driveTrain: Drivetrain = None,
        driverStation: wpilib.DriverStation = None,
    ):
        self.driverController = driverController
        self.mechController = mechController
        self.odometryPosition = driveTrain.odometry
        self.swerveModules = driveTrain.swerveModules
        self.driverStation = driverStation

        self.datalog = DataLog("data/log")
        for entryname, entrytype, logname in telemetryButtonEntries:
            setattr(self, "driver" + entryname, entrytype(self.datalog, "driver/" + logname))
            setattr(self, "mech" + entryname, entrytype(self.datalog, "mech/" + logname))
        for entryname, entrytype, logname in telemetryOdometryEntries:
            setattr(self, entryname, entrytype(self.datalog, "odometry/" + logname))
        for entryname, entrytype, logname in telemetrySwerveDriveTrainEntries:
            setattr(self, entryname, entrytype(self.datalog, "swervedrivetrain/" + logname))
        for entryname, entrytype, logname in driverStationEntries:
            setattr(self, entryname, entrytype(self.datalog, "driverstation/" + logname))

    def getDriverControllerInputs(self):
        """
        Records data for buttons and axis inputs for the first controller
        """
        self.driverAButton.append(self.driverController.getAButton()) #bool
        self.driverBButton.append(self.driverController.getBButton()) #bool
        self.driverXButton.append(self.driverController.getXButton()) #bool
        self.driverYButton.append(self.driverController.getYButton()) #bool
        self.driverBackButton.append(self.driverController.getBackButton()) #left side , bool
        self.driverStartButton.append(self.driverController.getStartButton()) #right side , bool
        self.driverLeftBumper.append(self.driverController.getLeftBumper()) #bool
        self.driverRightBumper.append(self.driverController.getRightBumper()) #bool
        self.driverLeftStickButton.append(self.driverController.getLeftStickButton()) #bool
        self.driverRightStickButton.append(self.driverController.getRightStickButton()) #bool
        self.driverLeftTrigger.append(self.driverController.getLeftTriggerAxis()) #float 0-1
        self.driverRightTrigger.append(self.driverController.getRightTriggerAxis()) #float 0-1
        self.driverJoystickLeftY.append(self.driverController.getLeftY()) #float -1-1
        self.driverJoystickLeftX.append(self.driverController.getLeftX()) #float -1-1
        self.driverJoystickRightY.append(self.driverController.getRightY()) #float -1-1
        self.driverJoystickRightX.append(self.driverController.getRightX()) #float -1-1
        self.driverDPad.append(self.driverController.getPOV()) #ints

    def getMechControllerInputs(self):
        """
        Records data for buttons and axis inputs for the second controller
        """
        self.mechAButton.append(self.mechController.getAButton()) #bool
        self.mechBButton.append(self.mechController.getBButton()) #bool
        self.mechXButton.append(self.mechController.getXButton()) #bool
        self.mechYButton.append(self.mechController.getYButton()) #bool
        self.mechBackButton.append(self.mechController.getBackButton()) #left side , bool
        self.mechStartButton.append(self.mechController.getStartButton()) #right side , bool
        self.mechLeftBumper.append(self.mechController.getLeftBumper()) #bool
        self.mechRightBumper.append(self.mechController.getRightBumper()) #bool
        self.mechLeftStickButton.append(self.mechController.getLeftStickButton()) #bool
        self.mechRightStickButton.append(self.mechController.getRightStickButton()) #bool
        self.mechLeftTrigger.append(self.mechController.getLeftTriggerAxis()) #float 0-1
        self.mechRightTrigger.append(self.mechController.getRightTriggerAxis()) #float 0-1
        self.mechJoystickLeftY.append(self.mechController.getLeftY()) #float -1-1
        self.mechJoystickLeftX.append(self.mechController.getLeftX()) #float -1-1
        self.mechJoystickRightY.append(self.mechController.getRightY()) #float -1-1
        self.mechJoystickRightX.append(self.mechController.getRightX()) #float -1-1
        self.mechDPad.append(self.mechController.getPOV()) #ints

    def getOdometryInputs(self):
        """
        Records the data for the positions of the bot in a field,
        Gives the x position, y position and rotation
        """
        pose = self.odometryPosition.getPose()
        self.xPositions.append(pose.X())
        self.yPositions.append(pose.Y())
        self.angles.append(pose.rotation().degrees())

    def getSwerveInputs(self):
        """
        Gets the inputs for some swerve drive train inputs
        it get the steer angle, the drive percent and the velocity
        """
        for i, swerveModule in enumerate(self.swerveModules):
            getattr(self, f"steerDegree{i + 1}").append(swerveModule.steerAngle)
            getattr(self, f"drivePercent{i + 1}").append(swerveModule.drivePercent)
            getattr(self, f"moduleVelocity{i + 1}").append(swerveModule.getDriveVelocity())
            getattr(self, f"currSteerDegree{i + 1}").append(math.degrees(swerveModule.getSteerAngle()))

    def getDriverStationInputs(self):
        """
        Gets the inputs of some match/general robot things,
        the things being: Alliance color and what mode it is in and
        if it is enabled
        """
        alliance = "No Alliance"
        if self.driverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
            alliance = "Blue"
        if self.driverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed:
            alliance = "Red"
        self.alliance.append(alliance)
        self.autonomous.append(self.driverStation.isAutonomous())
        self.teleop.append(self.driverStation.isTeleop())
        self.test.append(self.driverStation.isTest())
        self.enabled.append(self.driverStation.isEnabled())

    def runDataCollections(self):
        if self.driverController is not None:
            self.getDriverControllerInputs()
        if self.mechController is not None:
            self.getMechControllerInputs()
        if self.odometryPosition is not None:
            self.getOdometryInputs()
        if self.swerveModules is not None:
            self.getSwerveInputs()
        if self.driverStation is not None:
            self.getDriverStationInputs()
