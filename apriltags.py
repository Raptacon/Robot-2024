import random

from wpilib import ADIS16470_IMU
import wpilib
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.units import inchesToMeters
from wpimath.geometry import Pose2d, Rotation2d, Transform3d, Translation3d, Rotation3d
from subsystem.swerveDriveTrain import Drivetrain
from photonCamera import WrapperedPhotonCamera
class DrivePoseEstimator():
    CamPos = Transform3d(
        Translation3d(
            inchesToMeters(12.0), inchesToMeters(15.0), inchesToMeters(0.0)  # X  # Y  # Z
        ),
        Rotation3d(0.0, 0.0, 0.0),  # Roll  # Pitch  # Yaw
    )

    def __init__(self, drive : Drivetrain):
        self.curEstPose = Pose2d()
        self.curDesPose = Pose2d()
        self.gyro = ADIS16470_IMU()
        initialModuleStates =  drive.getModuleStates()
        self.kinematics = drive.getKinematics()

        self.cams = [
            WrapperedPhotonCamera("Arducam", self.CamPos),
        ]
        self.camTargetsVisible = False

        self.poseEst = SwerveDrive4PoseEstimator(
            self.kinematics, self._getGyroAngle(), initialModuleStates, self.curEstPose
        )
        self.lastModulePositions = initialModuleStates
        self.curRawGyroAngle = Rotation2d()

        self._simPose = Pose2d()

        self.useAprilTags = True

    def setKnownPose(self, knownPose):
        """Reset the robot's estimated pose to some specific position. This is useful if we know with certanty
        we are at some specific spot (Ex: start of autonomous)

        Args:
            knownPose (Pose2d): The pose we know we're at
        """
        if wpilib.TimedRobot.isSimulation():
            self._simPose = knownPose
            self.curRawGyroAngle = knownPose.rotation()

        self.poseEst.resetPosition(
            self.curRawGyroAngle, self.lastModulePositions, knownPose
        )

    def update(self, curModulePositions, curModuleSpeeds):
        """Periodic update, call this every 20ms.

        Args:
            curModulePositions (list[SwerveModuleState]): current module angle
            and wheel positions as read in from swerve module sensors
        """

        # Add any vision observations to the pose estimate
        self.camTargetsVisible = False

        if(self.useAprilTags):
            for cam in self.cams:
                cam.update(self.curEstPose)
                observations = cam.getPoseEstimates()
                for observation in observations:
                    self.poseEst.addVisionMeasurement(
                        observation.estFieldPose, observation.time
                    )
                    self.camTargetsVisible = True

        self.curRawGyroAngle = self._getGyroAngle()

        # Update the WPILib Pose Estimate
        self.poseEst.update(self.curRawGyroAngle, curModulePositions)
        self.curEstPose = self.poseEst.getEstimatedPosition()

        # Record the estimate to telemetry/logging-

        # Remember the module positions for next loop
        self.lastModulePositions = curModulePositions

    def getCurEstPose(self):
        """
        Returns:
            Pose2d: The most recent estimate of where the robot is at
        """
        return self.curEstPose
    
    def setUseAprilTags(self, use):
        self.useAprilTags = use

    # Local helper to wrap the real hardware angle into a Rotation2d
    def _getGyroAngle(self):
        return Rotation2d().fromDegrees(self.gyro.getAngle(self.gyro.getYawAxis()))