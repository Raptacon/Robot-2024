import wpilib
import json
import os
from pathlib import Path

#from wpilib.interfaces import GenericHID
import wpimath.filter
import wpimath
import commands2.button

from subsystem.swerveDriveTrain import Drivetrain

from commands.shortyIntake import Intake
from subsystem.sparkyIntake import SparkyIntake
from subsystem.sparkyIntakePivot import IntakePivot
from subsystem.sparkyIntakePivotController import pivotController

from commands.shortyShooter import ShooterCommand
from subsystem.sparkyShooter import Shooter
from subsystem.sparkyShooterPivot import ShooterPivot

from subsystem.sparkyLeds import Leds

from commands.defaultdrive import DefaultDrive
from commands.togglefielddrive import ToggleFieldDrive
from commands.resetfielddrive import ResetFieldDrive
from data.telemetry import Telemetry

from auto import SparkyShoot


from wpilib import CameraServer
kDriveControllerIdx = 0
kMechControllerIdx = 1
lastDeg =0

class RobotSwerve:
    """
    Container to hold the main robot code
    """

    def __init__(self) -> None:
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        self.driveController = wpilib.XboxController(kDriveControllerIdx)
        self.mechController = wpilib.XboxController(kMechControllerIdx)

        self.driveTrain = Drivetrain()

        # Provide access to the network communication data to / from the Driver Station.
        self.driverStation = wpilib.DriverStation

        self.intake = SparkyIntake()
        self.pivot = IntakePivot()
        self.intakePivotController = pivotController()
        self.intakePivotController.setIntakeRotationSubsystem(self.pivot)

        self.shooter = Shooter()
        self.shooterPivot = ShooterPivot()
        self.intakePivotController.calibrate()
        #self.driveController = wpilib.XboxController(0)

        self.xLimiter = wpimath.filter.SlewRateLimiter(3)
        self.yLimiter = wpimath.filter.SlewRateLimiter(3)
        self.rotLimiter = wpimath.filter.SlewRateLimiter(3)

        self.leds = Leds()

        commands2.button.JoystickButton(self.driveController, 1).onTrue(ToggleFieldDrive(self.driveTrain, lambda: True))
        commands2.button.JoystickButton(self.driveController, 2).onTrue(ResetFieldDrive(self.driveTrain))
        CameraServer.launch()

        # TODO - Default this to True once we like what we see with telemetry
        # By default, disable telemetry unless explicitly enabled by the drive station
        self.enableTelemetry = wpilib.SmartDashboard.getBoolean(
            "enableTelemetry", False
        )
        if self.enableTelemetry:
            self.telemetry = Telemetry(self.driveController, self.mechController, self.driveTrain, self.driverStation)

        '''
        self.driveTrain.setDefaultCommand(DefaultDrive(
            self.driveTrain,
            lambda: -self.driveController.getLeftY(),
            lambda: self.driveController.getLeftX(),
            lambda: -self.driveController.getRightX(),
            lambda: self.driveTrain.getFieldDriveRelative()
        ))'''

        # We should only need to do this once
        wpilib.SmartDashboard.putString("Robot Version", self.getDeployInfo("git-hash"))
        wpilib.SmartDashboard.putString("Git Branch", self.getDeployInfo("git-branch"))
        wpilib.SmartDashboard.putString(
            "Deploy Host", self.getDeployInfo("deploy-host")
        )
        wpilib.SmartDashboard.putString(
            "Deploy User", self.getDeployInfo("deploy-user")
        )
    def robotPeriodic(self) -> None:
        if self.enableTelemetry and self.telemetry:
            self.telemetry.runDataCollections()

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        pass

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.autonomousCommand = self.getAutonomousCommand()

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def getAutonomousCommand(self):
        return SparkyShoot(self.shooter, self.intake, self.driveTrain)

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""

    def teleopInit(self) -> None:
        # The below line toggles field drive on a button pressed. This is being replaced
        #  by the use of a held trigger
        ## commands2.button.JoystickButton(self.driveController, 1).onTrue(ToggleFieldDrive(self.driveTrain))
        commands2.button.JoystickButton(self.driveController, 6).onTrue(ToggleFieldDrive(self.driveTrain, lambda: True))
        commands2.button.JoystickButton(self.driveController, 6).onFalse(ToggleFieldDrive(self.driveTrain, lambda: False))
        commands2.button.JoystickButton(self.driveController, 2).onTrue(ResetFieldDrive(self.driveTrain))

        self.driveTrain.setDefaultCommand(DefaultDrive(
            self.driveTrain,
            lambda: wpimath.applyDeadband(self.driveController.getLeftX(), 0.06),
            lambda: wpimath.applyDeadband(self.driveController.getLeftY(), 0.06),
            lambda: wpimath.applyDeadband(self.driveController.getRightX(), 0.1),
            lambda: self.driveTrain.getFieldDriveRelative()
        ))
        self.intake.setDefaultCommand(Intake(
            self.intake,
            self.intakePivotController,
            lambda: wpimath.applyDeadband(self.mechController.getLeftTriggerAxis(), 0.05),
            lambda: self.mechController.getRightBumper(),
            lambda: self.mechController.getAButtonPressed(),
        ))

        self.shooter.setDefaultCommand(ShooterCommand(
            self.shooter,
            self.shooterPivot,
            lambda: self.mechController.getRightBumper(),
            lambda: self.mechController.getBButton(),
            lambda: self.mechController.getRightTriggerAxis(),
            self.mechController.getYButtonPressed,
            self.mechController.getXButton,
            self.mechController.getLeftBumper,
            self.mechController.getLeftY
        ))

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""
        pass

    testModes = ["Drive Disable",
                 "Wheels Select",
                 "Wheels Drive",
                 "Enable Cal",
                 "Disable Cal",
                 "Wheel Pos",
                 "Pivot Rot",
                 "Shooter Cal",
                 "Shoot Piviot Zero",
                 "Shoot Piviot Reverse",
                 "Shoot Piviot Pos"]

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        #commands2.CommandScheduler.getInstance().cancelAll()
        self.calEn = False
        self.calDis = False
        self.testChooser = wpilib.SendableChooser()
        for i in self.testModes:
            self.testChooser.addOption(i, i)
        self.testChooser.setDefaultOption("Drive Disable","Drive Disable")
        wpilib.SmartDashboard.putData("Test Mode", self.testChooser)
        wpilib.SmartDashboard.putNumber("Wheel Angle", 0)
        wpilib.SmartDashboard.putNumber("Wheel Speed", 0)
        wpilib.SmartDashboard.putNumber("Pivot Angle:", 0.5)
        wpilib.SmartDashboard.putNumber("Shooter Angle:", 310)


    def testPeriodic(self) -> None:
        wheelAngle = wpilib.SmartDashboard.getNumber("Wheel Angle", 0) # noqa: E117,F841
        wheelSpeed = wpilib.SmartDashboard.getNumber("Wheel Speed", 0) # noqa: E117,F841
        pivotAngle = wpilib.SmartDashboard.getNumber("Pivot Angle:", 0.5) # noqa: E117,F841
        shooterAngle = wpilib.SmartDashboard.putNumber("Shooter Angle:", 310) # noqa: E117,F841
        wheelAngle #"use" value
        wheelSpeed #"use" value
        self.driveTrain.getCurrentAngles()
        global lastDeg

        #self.driveTrain.drive(-1 * LeftY * self.MaxMps, LeftX * self.MaxMps, RightX * self.RotationRate, False)
        match self.testChooser.getSelected():
            case "Drive Disable":
                print("Drive Disable")
                self.calEn = False
                self.calDis = False
                self.driveTrain.disable()
            case "Wheels Select":
                self.driveTrain.setSteer(wheelAngle)
            case "Wheels Drive":
                self.driveTrain.setDrive(wheelSpeed)
            case "Enable Cal":
                if not self.calEn:
                    self.driveTrain.calWheels(True)
                    self.calEn = False
            case "Disable Cal":
                self.driveTrain.calWheels(False)
            case "Wheel Pos":
                self.driveTrain.setSteer(wheelAngle)
            case "Pivot Rot":
                self.intakePivotController.setManipulator(pivotAngle)
            case "Shoot Piviot Zero":
                self.shooterPivot.zeroPivot(0.2)
            case "Shoot Piviot Reverse":
                self.shooterPivot.maxPivot(0.2)
            case "Shoot Piviot Pos":
                self.shooterPivot.enable()
                self.shooterPivot.setSetpoint(pivotAngle)
                self.shooterPivot.periodic()
                pass
            case _:
                print(f"Unknown {self.testChooser.getSelected()}")

        for m in self.driveTrain.swerveModules:
            break
            print(f"{m.name} {m.driveMotor.getAppliedOutput()} {m.driveMotor.get()}")

    def getDeployInfo(self, key: str) -> str:
        """Gets the Git SHA of the deployed robot by parsing ~/deploy.json and returning the git-hash from the JSON key OR if deploy.json is unavilable will return "unknown"
           example deploy.json: '{"deploy-host": "DESKTOP-80HA89O", "deploy-user": "ehsra", "deploy-date": "2023-03-02T17:54:14", "code-path": "blah", "git-hash": "3f4e89f138d9d78093bd4869e0cac9b61becd2b9", "git-desc": "3f4e89f-dirty", "git-branch": "fix-recal-nbeasley"}

        Args:
            key (str): The desired json key to get. Popular onces are git-hash, deploy-host, deploy-user

        Returns:
            str: Returns the value of the desired deploy key
        """
        json_object = None
        home = str(Path.home()) + os.path.sep
        releaseFile = home + 'py' + os.path.sep + "deploy.json"
        try:
            # Read from ~/deploy.json
            with open(releaseFile, "r") as openfile:
                json_object = json.load(openfile)
                print(json_object)
                print(type(json_object))
                if key in json_object:
                    return json_object[key]
                else:
                    return f"Key: {key} Not Found in JSON"
        except OSError:
            return "unknown"
        except json.JSONDecodeError:
            return "bad json in deploy file check for unescaped "
