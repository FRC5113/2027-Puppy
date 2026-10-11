from __future__ import annotations

from mode_robot.modes import TeleopMode
from subsystems.drivetrain.drivetrain import Drivetrain

from lemonlib.smart.preference import SmartPreference
from lemonlib.control import LemonInput


class Teleop(TeleopMode):
    """
    The teleop mode implementation for the robot.
    """
    def __init__(self, drivetrain: Drivetrain, controller: LemonInput) -> None:
        self._drivetrain = drivetrain
        self._controller = controller

        self.forward_deadband = SmartPreference("Teleop/ForwardDeadband", 0.1)
        self.angular_deadband = SmartPreference("Teleop/AngularDeadband", 0.1)

    def _deadband(self, value: float, threshold: float) -> float:
        if abs(value) < threshold:
            return 0.0
        return value

    def on_periodic(self) -> None:
        forward_percent = self._deadband(-self._controller.getLeftY(), self.forward_deadband.get())
        angular_percent = self._deadband(-self._controller.getRightX(), self.angular_deadband.get())

        self._drivetrain.drive(forward_percent, angular_percent)
