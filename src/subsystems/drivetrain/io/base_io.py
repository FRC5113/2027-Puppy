from __future__ import annotations

from abc import ABC, abstractmethod

from wpimath.geometry import Pose2d


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
    def set_left_percent(self, percent: float) -> None:
        """
        Sets a percent to the left side of the drivetrain.
        """
        ...

    @abstractmethod
    def set_right_percent(self, percent: float) -> None:
        """
        Sets a percent to the right side of the drivetrain.
        """
        ...

    def update(self) -> None:
        """
        Optional lifecycle hook to update the state of the IO if necessary.
        """
        pass
