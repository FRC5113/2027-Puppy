from __future__ import annotations

from wpilib import XboxController

from mode_robot.modes import TeleopMode
from subsystems.drivetrain import Drivetrain


class Teleop(TeleopMode):
    """
    The teleop mode implementation for the robot.
    """
    def __init__(self, drivetrain: Drivetrain, controller: XboxController) -> None:
        """
        Initializes the teleop mode with subsystem implementations & a controller.
        """
        self._drivetrain = drivetrain
        self._controller = controller
    
    def on_periodic(self) -> None:
        forward_percent = -self._controller.getLeftY()
        angular_percent = -self._controller.getRightX()

        self._drivetrain.drive(forward_percent, angular_percent)
