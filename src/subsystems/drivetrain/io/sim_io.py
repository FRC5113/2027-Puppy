from __future__ import annotations

from wpilib import Timer
from wpilib.simulation import DifferentialDrivetrainSim
from wpimath.geometry import Pose2d

from subsystems.drivetrain.io.base_io import DrivetrainBaseIO
from subsystems.drivetrain.constants import DrivetrainConstants

BATTERY_VOLTAGE = 12.0


class DrivetrainSimIO(DrivetrainBaseIO):
    """
    A simulated IO that allows the bot to run without real hardware.
    """
    def __init__(self) -> None:
        self._diff_drive_sim = DifferentialDrivetrainSim(
            driveMotor=DrivetrainConstants.motor_shaft,
            trackWidth=DrivetrainConstants.track_width,
            gearing=DrivetrainConstants.gear_ratio,
            J=DrivetrainConstants.MOI,
            mass=DrivetrainConstants.mass,
            wheelRadius=DrivetrainConstants.wheel_radius,
        )

        # The timestamp in seconds for the previous iteration.
        # This is used to update the differential drive simulation every iteration.
        self._previous_timestamp = 0.0

        self._desired_left_percent = 0.0
        self._desired_right_percent = 0.0

    def get_pose(self) -> Pose2d | None:
        return self._diff_drive_sim.getPose()

    def set_left_percent(self, percent: float) -> None:
        self._desired_left_percent = percent

    def set_right_percent(self, percent: float) -> None:
        self._desired_right_percent = percent

    def update(self) -> None:
        self._diff_drive_sim.setInputs(
            leftVoltage=self._desired_left_percent * BATTERY_VOLTAGE,
            rightVoltage=self._desired_right_percent * BATTERY_VOLTAGE
        )

        current_timestamp = Timer.getFPGATimestamp()
        delta_timestamp = current_timestamp - self._previous_timestamp
        self._diff_drive_sim.update(delta_timestamp)

        self._previous_timestamp = current_timestamp
