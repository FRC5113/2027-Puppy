from __future__ import annotations

from typing import Any

from wpimath.filter import SlewRateLimiter

from mode_robot.modes import TeleopMode
from subsystems.drivetrain import Drivetrain

from lemonlib.smart.preference import SmartPreference
from lemonlib.control import LemonInput

# pyright: reportUnknownMemberType=false
# pyright: reportArgumentType=false


class ValueTracker:
    """
    Tracks if any value has changed or not.
    """
    def __init__(self, value: Any) -> None:
        self.value = value

    def update(self, new_value: Any) -> bool:
        """
        Returns `True` if the value has changed.
        """
        changed = new_value != self.value
        self.value = new_value
        return changed


class Teleop(TeleopMode):
    """
    The teleop mode implementation for the robot.
    """
    forward_slew_enabled = SmartPreference(False)
    forward_slew = SmartPreference(0.0)
    forward_deadband = SmartPreference(0.1)

    angular_slew_enabled = SmartPreference(False)
    angular_slew = SmartPreference(0.0)
    angular_deadband = SmartPreference(0.1)

    def __init__(self, drivetrain: Drivetrain, controller: LemonInput) -> None:
        """
        Initializes the teleop mode with subsystem implementations & a controller.
        """
        self._drivetrain = drivetrain
        self._controller = controller

        self._forward_slew = SlewRateLimiter(self.forward_slew)
        self._angular_slew = SlewRateLimiter(self.angular_slew)

        self._forward_slew_tracker = ValueTracker(self.forward_slew)
        self._angular_slew_tracker = ValueTracker(self.angular_slew)

    def _deadband(self, value: float, threshold: float) -> float:
        """
        Applies a deadband to a joystick percentage value.
        """
        if abs(value) < threshold:
            return 0.0
        return value

    def on_periodic(self) -> None:
        """
        Every iteration, retrieves the percentages from a `LemonController` and
        applies slew rate limiting if applicable.
        """
        forward_percent = -self._controller.getLeftY()
        angular_percent = -self._controller.getRightX()

        if self.forward_slew_enabled:
            # If the value for the forward limiter changed, create a new limiter object.
            if self._forward_slew_tracker.update(self.forward_slew):
                self._forward_slew = SlewRateLimiter(self.forward_slew)

            forward_percent = self._forward_slew.calculate(forward_percent)
        
        if self.angular_slew_enabled:
            # If the value for the angular limiter changed, create a new limiter object.
            if self._angular_slew_tracker.update(self.angular_slew):
                self._angular_slew = SlewRateLimiter(self.angular_slew)

            angular_percent = self._angular_slew.calculate(angular_percent)

        forward_percent = self._deadband(forward_percent, self.forward_deadband)
        angular_percent = self._deadband(angular_percent, self.angular_deadband)

        self._drivetrain.drive(forward_percent, angular_percent)
