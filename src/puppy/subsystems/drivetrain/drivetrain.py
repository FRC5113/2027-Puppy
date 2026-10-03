from __future__ import annotations

from wpilib import RobotController

from wpimath.kinematics import DifferentialDriveKinematics, ChassisSpeeds
from wpimath.geometry import Pose2d
from wpimath.units import percent

from puppy.subsystems.base import Subsystem
from puppy.subsystems.drivetrain.constants import DrivetrainConstants
from puppy.subsystems.drivetrain.io.base_io import DrivetrainBaseIO


class Drivetrain(Subsystem):
    """
    The base of the robot that allows the bot to actually drive around.
    """
    def __init__(self, io: DrivetrainBaseIO) -> None:
        """
        Initializes the drivetrain with an IO implementation.
        """
        self._io = io
        self._kinematics = DifferentialDriveKinematics(DrivetrainConstants.track_width)

        self._forward_percent = 0.0
        self._angular_percent = 0.0

    def get_pose(self) -> Pose2d | None:
        """
        Returns the robot pose, if applicable.

        Returns `None` upon real hardware being used (there are no encoders to measure
        the actual drivetrain pose).
        """
        return self._io.get_pose()

    def drive(self, forward_percent: percent, angular_percent: percent) -> None:
        """
        Requests values to drive the robot with.
        
        Args:
            forward_percent: The forward percent [-1, 1] to request.
            angular_percent: The angular percent [-1, 1] to request.
        """
        self._forward_percent = forward_percent
        self._angular_percent = angular_percent

    def update(self) -> None:
        """
        Updates the state of the subsystem after all values were requested.
        """
        vx = self._forward_percent * DrivetrainConstants.max_linear_speed
        omega = self._angular_percent * DrivetrainConstants.max_angular_speed

        chassis = ChassisSpeeds(vx, 0.0, omega)
        wheel_speeds = self._kinematics.toWheelSpeeds(chassis)
        wheel_speeds.desaturate(DrivetrainConstants.max_linear_speed)

        left_percent = wheel_speeds.left / DrivetrainConstants.max_linear_speed
        right_percent = wheel_speeds.right / DrivetrainConstants.max_linear_speed

        left_voltage = left_percent * RobotController.getBatteryVoltage()
        right_voltage = right_percent * RobotController.getBatteryVoltage()

        self._io.set_left_voltage(left_voltage)
        self._io.set_right_voltage(right_voltage)

        self._forward_percent = 0.0
        self._angular_percent = 0.0
