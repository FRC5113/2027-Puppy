from __future__ import annotations

from abc import ABC, abstractmethod

from wpimath.geometry import Rotation2d, Pose2d


class DrivetrainBaseIO(ABC):
    """
    The base IO, containing all of the methods that subclass IOs must implement.
    """
    @abstractmethod
    def get_pose(self) -> Pose2d | None:
        """
        Returns the full robot pose of the drivetrain, if possible.
        """
        ...

    @abstractmethod
    def get_angle(self) -> Rotation2d:
        """
        Returns the angle of the gyro.
        """
        ...

    @abstractmethod
    def set_left_voltage(self, volts: float) -> None:
        """
        Sets a raw voltage to the left side of the drivetrian.
        """
        ...

    @abstractmethod
    def set_right_voltage(self, volts: float) -> None:
        """
        Sets a raw voltage to the right side of the drivetrian.
        """
        ...

    def update(self) -> None:
        """
        Optional lifecycle hook to update the state of the IO if necessary.
        """
        pass
