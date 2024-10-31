import navx
from swerve.swerveModule import SwerveModuleMk4L1SparkMaxNeoCanCoder as SwerveModule

import commands2
import wpimath.kinematics
from wpimath.kinematics import ChassisSpeeds
import wpimath.geometry
from wpimath.geometry import Rotation2d
from wpimath.geometry import Pose2d
import math
import wpilib

from pathplannerlib.auto import AutoBuilder
from pathplannerlib.config import HolonomicPathFollowerConfig, ReplanningConfig, PIDConstants
from pathplannerlib.path import PathPlannerPath
from pathplannerlib.commands import FollowPathHolonomic

from wpilib import DriverStation

import ntcore

class AutoDrivetrain(commands2.SubsystemBase):
    kMaxVoltage = 12.0
    kWheelBaseMeters = 0.7112 # front to back distance
    kTrackBaseMeters = 0.6604 # left to right distance
    #kMaxVelocityMPS = 4.14528
    kMaxVelocityMPS = 1.0
    chassisSpeeds = wpimath.kinematics.ChassisSpeeds
    kMaxAngularVelocityRadPS = kMaxVelocityMPS / math.hypot(kWheelBaseMeters / 2.0, kTrackBaseMeters / 2.0)

    kModuleProps = [
            {"name": "frontLeft", "channel": 50, "encoderCal": 83.496, "trackbase": kTrackBaseMeters/2.0, "wheelbase": kWheelBaseMeters/2.0, "inverted": False,  },
            {"name": "frontRight", "channel": 53, "encoderCal": 356.396, "trackbase": -kTrackBaseMeters/2.0, "wheelbase": kWheelBaseMeters/2.0, "inverted": False },
            {"name": "rearLeft", "channel": 56, "encoderCal": 50.098, "trackbase": kTrackBaseMeters/2.0, "wheelbase": -kWheelBaseMeters/2.0, "inverted": False },
            {"name": "rearRight", "channel": 59, "encoderCal": 69.785, "trackbase": -kTrackBaseMeters/2.0, "wheelbase": -kWheelBaseMeters/2.0, "inverted": False  }
    ]
    kModulePropsNoCal = [
            {"name": "frontLeft", "channel": 50, "encoderCal": 0.0, "trackbase": kTrackBaseMeters/2.0, "wheelbase": kWheelBaseMeters/2.0, "inverted": False },
            {"name": "frontRight", "channel": 53, "encoderCal": 0.0, "trackbase": -kTrackBaseMeters/2.0, "wheelbase": kWheelBaseMeters/2.0, "inverted": True },
            {"name": "rearLeft", "channel": 56, "encoderCal": 0.0, "trackbase": kTrackBaseMeters/2.0, "wheelbase": -kWheelBaseMeters/2.0, "inverted": False },
            {"name": "rearRight", "channel": 59, "encoderCal": 0.0, "trackbase": -kTrackBaseMeters/2.0, "wheelbase": -kWheelBaseMeters/2.0, "inverted": True }
    ]


#52 - -181.2
#58 -  128.0
#55 - -294.4
#61 - -273.4

#new offests as of 6/30/2023 for swerve chasis
#52 - 31.992
#55 - 153.193
#58 - -23.555
#61 - 34.717
    def __init__(self):
        super().__init__()
        self.swerveModules = list[SwerveModule]()
        self.datatable = ntcore.NetworkTableInstance.getDefault()
        self.table = self.datatable.getTable("Drivetrain")
        self.posTable = self.datatable.getTable("Robot position")
        assert(self.table)
        for module in AutoDrivetrain.kModuleProps:
            name = module["name"]
            subTable = self.table.getSubTable(name)
            assert(subTable)
            wheelbase = module["wheelbase"]
            trackbase = module["trackbase"]
            channel = module["channel"]
            encoderCal = module["encoderCal"]
            inverted = module["inverted"]
            self.swerveModules.append(SwerveModule((trackbase, wheelbase, name), channel, inverted, encoderCal, subTable))

        self.imu = navx.AHRS.create_spi()

        self.kinematics = wpimath.kinematics.SwerveDrive4Kinematics(
            self.swerveModules[1].getTranslation(),
            self.swerveModules[3].getTranslation(),
            self.swerveModules[0].getTranslation(),
            self.swerveModules[2].getTranslation(),
        )

        self.moduleRotations = []
        for module in self.swerveModules:
            self.moduleRotations.append(module.getPosition())
        self.moduleRotations = tuple(self.moduleRotations)

        self.headingOffset = 0
        self.odometry = wpimath.kinematics.SwerveDrive4Odometry(self.kinematics, self.getHeading(), self.moduleRotations)
        self.pos = Pose2d()
        self.posX = 0
        self.posY = 0
        self.setFieldDriveRelative(True)
        self.ang = 0
        self.iteration = 0
        
        AutoBuilder.configureHolonomic(
            self.getPose, # Robot pose supplier
            self.resetPose, # Method to reset odometry (will be called if your auto has a starting pose)
            self.getRobotRelativeSpeeds(), # ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
            self.runVelocity, # Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds
            HolonomicPathFollowerConfig( # HolonomicPathFollowerConfig, this should likely live in your Constants class
                PIDConstants(0.05, 0.0, 0.0), # Translation PID constants
                PIDConstants(0.2, 0.0, 0.1), # Rotation PID constants
                self.kMaxVelocityMPS, # Max module speed, in m/s
                self.kTrackBaseMeters, # Drive base radius in meters. Distance from robot center to furthest module.
                ReplanningConfig() # Default path replanning config. See the API for the options here
            ),
            self.shouldFlipPath, # Supplier to control path flipping based on alliance color
            self # Reference to this subsystem to set requirements
        )


    def shouldFlipPath(self):
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed

    def getHeading(self) -> Rotation2d:
        return Rotation2d.fromDegrees(self.imu.getFusedHeading() - self.headingOffset)

    def resetPose(self):
        self.headingOffset = self.imu.getFusedHeading()
        self.resetOdometry()

    def driveRobotRelative(self, chassisSpeeds : ChassisSpeeds):
        for mod, speed in zip(self.swerveModules, chassisSpeeds):
            print(speed)
            mod.setDriveVoltage(speed)

        self.updateOdometry()
        self.setChassisSpeeds(chassisSpeeds)

    def updateOdometry(self):
        self.pos = self.odometry.update(self.getHeading(),
                            [self.swerveModules[1].getPosition(),
                            self.swerveModules[3].getPosition(),
                            self.swerveModules[0].getPosition(),
                            self.swerveModules[2].getPosition()])
         
        self.posX = self.pos.Y()
        self.posY = self.pos.X()

        if self.posTable:
            self.posTable.putNumber("Robot_PosX", self.pos.Y())
            self.posTable.putNumber("Robot_PosY", self.pos.X())
            self.posTable.putNumber("Robot_Angle", self.pos.rotation().degrees())
        else:
            self.posTable = self.datatable.getTable("Robot position")
    
    def getRobotRelativeSpeeds(self) -> ChassisSpeeds:
        return self.chassisSpeeds

    def setChassisSpeeds(self, chassisSpeeds):
        self.chassisSpeeds = chassisSpeeds

    def resetOdometry(self):
        self.odometry.resetPosition(self.getHeading(),
                            [self.swerveModules[1].getPosition(),
                            self.swerveModules[3].getPosition(),
                            self.swerveModules[0].getPosition(),
                            self.swerveModules[2].getPosition()],
                            Pose2d()
                            )
        
    def getPose(self) -> Pose2d:
        return self.pos
        
    def disable(self, steer = True, drive = True):
        for m in self.swerveModules:
            m.disable(steer, drive)

    def setSteer(self, angle : float):
        angle %= 360
        for m in self.swerveModules:
            m.setSteerAngle(angle)

    def getCurrentAngles(self):
        angles = []
        for m in self.swerveModules:
            angle = m.getCurrentAngle()
            wpilib.SmartDashboard.putNumber(f"{m.cancoderId}Pos", angle)
            angles.append(angle)
        return angles

    def setDrive(self, speedPercent: float):
        for m in self.swerveModules:
            m.setDrivePercent(speedPercent)

    def runVelocity(self, speeds : ChassisSpeeds):
        discreteSpeeds = ChassisSpeeds.discretize(speeds, 0.002)

        setPointStates = self.kinematics.toSwerveModuleStates(discreteSpeeds)
        self.kinematics.desaturateWheelSpeeds(setPointStates, self.kMaxVelocityMPS)

        for mod, state in zip(self.swerveModules, setPointStates):
            mod.runSetpoint(state)

        self.updateOdometry()

        print(self.getPose())

    def setFieldDriveRelative(self, state: bool):
        self.fieldRelative = state
        wpilib.SmartDashboard.putBoolean("Field Relative", state)

    def getFieldDriveRelative(self) -> bool:
        return self.fieldRelative

    def calWheels(self, enable):
        for m in self.swerveModules:
            m.setCal(enable)

    """Future improvment"""
    #def periodic(self):
    #    for m in self.swerveModules:
    #        m.periodic()
