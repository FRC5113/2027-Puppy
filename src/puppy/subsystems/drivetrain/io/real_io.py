from __future__ import annotations

from phoenix5 import TalonSRX, ControlMode, NeutralMode

from wpilib import RobotController
from wpimath.geometry import Pose2d

from puppy.subsystems.drivetrain.io.base_io import DrivetrainBaseIO
from puppy.subsystems.drivetrain.constants import DrivetrainConstants


class DrivetrainRealIO(DrivetrainBaseIO):
    """
    The real IO, containing actual hardware implementations for talonSRX's.
    """
    def __init__(self) -> None:
        """
        Initializes the hardware for the real IO.
        """
        self._front_left_motor = TalonSRX(DrivetrainConstants.CAN.front_left)
        self._front_right_motor = TalonSRX(DrivetrainConstants.CAN.front_right)
        self._back_left_motor = TalonSRX(DrivetrainConstants.CAN.back_left)
        self._back_right_motor = TalonSRX(DrivetrainConstants.CAN.back_right)

        self._front_right_motor.setInverted(True)
        self._front_left_motor.setInverted(True)

        self._back_left_motor.follow(self._front_left_motor)
        self._back_right_motor.follow(self._front_right_motor)

        self._front_left_motor.setNeutralMode(NeutralMode.Brake)
        self._front_right_motor.setNeutralMode(NeutralMode.Brake)

    def get_pose(self) -> Pose2d | None:
        """
        Always returns `None` because no sensors can measure the pose of the real robot.
        """
        return None

    def set_left_voltage(self, volts: float) -> None:
        """
        Sets a voltage to both left motors.
        """
        battery_voltage = RobotController.getBatteryVoltage()
        self._front_left_motor.set(ControlMode.PercentOutput, volts / battery_voltage)

    def set_right_voltage(self, volts: float) -> None:
        """
        Sets a voltage to both right motors.
        """
        battery_voltage = RobotController.getBatteryVoltage()
        self._front_right_motor.set(ControlMode.PercentOutput, volts / battery_voltage)
