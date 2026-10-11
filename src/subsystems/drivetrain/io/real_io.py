from __future__ import annotations

from phoenix5 import TalonSRX, ControlMode

from wpimath.geometry import Pose2d

from subsystems.drivetrain.io.base_io import DrivetrainBaseIO
from subsystems.drivetrain.constants import DrivetrainConstants

from hardware.motor_config import MotorConfig


class DrivetrainRealIO(DrivetrainBaseIO):
    """
    The real IO, containing actual hardware implementations for TalonSRX's.
    """
    def __init__(self) -> None:
        self._front_left_motor = TalonSRX(DrivetrainConstants.CAN.front_left)
        self._front_right_motor = TalonSRX(DrivetrainConstants.CAN.front_right)
        self._back_left_motor = TalonSRX(DrivetrainConstants.CAN.back_left)
        self._back_right_motor = TalonSRX(DrivetrainConstants.CAN.back_right)

        MotorConfig().apply(self._front_left_motor)
        MotorConfig().apply(self._back_left_motor)
        MotorConfig(inverted=True).apply(self._front_right_motor)
        MotorConfig(inverted=True).apply(self._back_right_motor)

    def get_pose(self) -> Pose2d | None:
        # Always returns `None` because no sensors can measure the pose of the real robot.
        return None

    def set_left_percent(self, percent: float) -> None:
        self._front_left_motor.set(ControlMode.PercentOutput, percent)
        self._back_left_motor.set(ControlMode.PercentOutput, percent)

    def set_right_percent(self, percent: float) -> None:
        self._front_right_motor.set(ControlMode.PercentOutput, percent)
        self._back_right_motor.set(ControlMode.PercentOutput, percent)
