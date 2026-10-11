from __future__ import annotations

from wpilib.drive import DifferentialDrive

from wpimath.kinematics import DifferentialDriveKinematics
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

        self._forward_scaler = SmartPreference("Drivetrain/ForwardScaler", 1.0)
        self._angular_scaler = SmartPreference("Drivetrain/AngularScaler", 1.0)

    def get_pose(self) -> Pose2d | None:
        """
        Returns the robot pose, if applicable.
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
        speeds = DifferentialDrive.arcadeDriveIK(forward_percent, angular_percent, squareInputs=False)

        self._io.set_left_percent(speeds.left)
        self._io.set_right_percent(speeds.right)

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
        forward_pct = self._forward_scaler.get() * self._forward_percent
        angular_pct = self._angular_scaler.get() * self._angular_percent

        self._command_motor_voltages(forward_pct, angular_pct)

        self._forward_percent = 0.0
        self._angular_percent = 0.0

        self._publish_telemetry()
