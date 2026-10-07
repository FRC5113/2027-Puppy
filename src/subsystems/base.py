from __future__ import annotations

from abc import ABC, abstractmethod


class Subsystem(ABC):
    """
    A single encapsulated mechanism for a robot.
    """
    @abstractmethod
    def update(self) -> None:
        """
        Updates and executes the state of the subsystem every iteration.
        """
        ...
