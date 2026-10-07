from __future__ import annotations

from wpilib import RobotController

from wpimath.kinematics import DifferentialDriveKinematics, ChassisSpeeds
from wpimath.geometry import Pose2d, Pose3d
from wpimath.units import percent

from ntcore import NetworkTableInstance

from subsystems.base import Subsystem
from subsystems.drivetrain.constants import DrivetrainConstants
from subsystems.drivetrain.io.base_io import DrivetrainBaseIO

from lemonlib.smart.preference import SmartPreference


class Drivetrain(Subsystem):
    """
    The base of the robot that allows the bot to actually drive around.
    """
    forward_scaler = SmartPreference(1.0)
    angular_scaler = SmartPreference(1.0)

    def __init__(self, io: DrivetrainBaseIO) -> None:
        """
        Initializes the drivetrain with an IO implementation.
        """
        self._io = io
        self._kinematics = DifferentialDriveKinematics(DrivetrainConstants.track_width)

        self._forward_percent = 0.0
        self._angular_percent = 0.0

        # Used for telemetry to allow for the robot to be represented in 3D.
        self._robot_pose_publisher = NetworkTableInstance.getDefault() \
            .getStructTopic("/SmartDashboard/Drivetrain/RobotPose3d", Pose3d) \
            .publish()

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

    def _command_motor_voltages(self, forward_percent: float, angular_percent: float) -> None:
        """
        Commands motor voltages to the left and right motors given a forward percent & angular percent.
        """
        vx = forward_percent * DrivetrainConstants.max_linear_speed
        omega = angular_percent * DrivetrainConstants.max_angular_speed

        chassis = ChassisSpeeds(vx, 0.0, omega)
        wheel_speeds = self._kinematics.toWheelSpeeds(chassis)
        wheel_speeds.desaturate(DrivetrainConstants.max_linear_speed)

        left_percent = wheel_speeds.left / DrivetrainConstants.max_linear_speed
        right_percent = wheel_speeds.right / DrivetrainConstants.max_linear_speed

        left_voltage = left_percent * RobotController.getBatteryVoltage()
        right_voltage = right_percent * RobotController.getBatteryVoltage()

        self._io.set_left_voltage(left_voltage)
        self._io.set_right_voltage(right_voltage)

    def _publish_telemetry(self) -> None:
        """
        Publishes all of the telemetry for the drivetrain / drivetrain IO.
        """
        pose = self.get_pose()
        if pose is not None:
            self._robot_pose_publisher.set(Pose3d(pose))

    def update(self) -> None:
        """
        Updates the state of the subsystem after all values were requested.
        """
        forward_pct = float(self.forward_scaler * self._forward_percent)    # type: ignore[unknownType]
        angular_pct = float(self.angular_scaler * self._angular_percent)    # type: ignore[unknownType]

        self._command_motor_voltages(forward_pct, angular_pct)

        self._forward_percent = 0.0
        self._angular_percent = 0.0

        self._publish_telemetry()
