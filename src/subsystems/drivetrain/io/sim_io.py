from __future__ import annotations

from wpilib import Timer
from wpilib.simulation import DifferentialDrivetrainSim
from wpimath.geometry import Pose2d

from subsystems.drivetrain.io.base_io import DrivetrainBaseIO
from subsystems.drivetrain.constants import DrivetrainConstants


class DrivetrainSimIO(DrivetrainBaseIO):
    """
    A simulated IO that allows the bot to run without real hardware.
    """
    def __init__(self) -> None:
        """
        Initializes the simulation hardware and state of the IO.
        """
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

        self._desired_left_voltage = 0.0
        self._desired_right_voltage = 0.0

    def get_pose(self) -> Pose2d | None:
        """
        Returns the current simulated robot pose.
        """
        return self._diff_drive_sim.getPose()

    def set_left_voltage(self, volts: float) -> None:
        """
        Sets the internal left voltage to be commanded once the IO is updated.
        """
        self._desired_left_voltage = volts

    def set_right_voltage(self, volts: float) -> None:
        """
        Sets the internal right voltage to be commanded once the IO is updated.
        """
        self._desired_right_voltage = volts

    def update(self) -> None:
        """
        Updates the state of the differential drive sim every iteration.
        """
        self._diff_drive_sim.setInputs(
            leftVoltage=self._desired_left_voltage,
            rightVoltage=self._desired_right_voltage
        )

        current_timestamp = Timer.getFPGATimestamp()
        delta_timestamp = current_timestamp - self._previous_timestamp
        self._diff_drive_sim.update(delta_timestamp)

        self._previous_timestamp = current_timestamp

        self._desired_left_voltage = 0.0
        self._desired_right_voltage = 0.0
