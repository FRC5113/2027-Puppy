from __future__ import annotations

from wpimath.system.plant import DCMotor
from wpimath.units import (
    meters, 
    meters_per_second, 
    radians_per_second,
    kilograms, 
    kilogram_square_meters
)


class DrivetrainConstants:
    """
    Holds all of the drivetrain-specific constants for both simulation & the physical bot.
    """
    motor_shaft = DCMotor.CIM(2)
    MOI: kilogram_square_meters = 6.0
    mass: kilograms = 45.2
    wheel_radius: meters = 0.0805
    track_width: meters = 0.6
    gear_ratio: float = 10.71   # ratio between the motor & wheels

    max_linear_speed: meters_per_second = 4.2
    max_angular_speed: radians_per_second = 9.6

    class CAN:
        """
        Holds the CAN ids for all physical hardware.
        """
        front_left = 1
        front_right = 2
        back_left = 3
        back_right = 4
