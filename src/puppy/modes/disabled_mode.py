from __future__ import annotations

from mode_robot.modes import DisabledMode

from puppy.subsystems.drivetrain import Drivetrain


class Disabled(DisabledMode):
    """
    The disabled mode implementation for the robot.
    """
    def __init__(self, drivetrain: Drivetrain) -> None:
        """
        Initializes the disabled mode with subsystem implementations.
        """
        self._drivetrain = drivetrain

    def on_enter(self) -> None:
        self._drivetrain.drive(0.0, 0.0)
    
    def on_periodic(self) -> None:
        self._drivetrain.drive(0.0, 0.0)

    def on_exit(self) -> None:
        self._drivetrain.drive(0.0, 0.0)
