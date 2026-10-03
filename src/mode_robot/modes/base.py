from __future__ import annotations

from abc import ABC


class Mode(ABC):
    """
    A base class that declares something as a possible mode of execution for a robot.

    All modes can declare lifecycle methods for when they are entered, 
    executed periodically, and exited.
    """
    def on_enter(self) -> None:
        """
        Called once upon this mode being entered.
        """
        pass

    def on_periodic(self) -> None:
        """
        Called every iteration upon being in this mode.
        """
        pass

    def on_exit(self) -> None:
        """
        Called upon this mode being exited.
        """
        pass
