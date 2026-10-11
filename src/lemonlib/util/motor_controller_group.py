from wpilib.interfaces import MotorController

from typing import SupportsFloat, SupportsIndex, Iterable


class MotorControllerGroup(MotorController):
    """
    A grouping of motor controllers that follow a lead motor controller.
    All commands / configurations to a motor controller are commanded to its followers.
    """
    _is_inverted: bool = False

    def __init__(
        self, 
        lead_controller: MotorController, 
        following_controllers: Iterable[MotorController]
    ) -> None:
        """
        Creates a new MotorControllerGroup with the provided MotorControllers.

        Args:
            lead_controller: The leading motor controller that all other controllers will follow.
            following_controllers: The following motor controllers.
        """
        MotorController.__init__(self)

        self._motor_controllers = [lead_controller] + list(following_controllers)

        self._is_inverted = False

    def set(self, speed: SupportsFloat | SupportsIndex) -> None:
        for mc in self._motor_controllers:
            mc.set(-float(speed) if self._is_inverted else float(speed))

    def setVoltage(self, output: float):
        for mc in self._motor_controllers:
            mc.setVoltage(-output if self._is_inverted else output)

    def get(self) -> float:
        if len(self._motor_controllers) > 0:
            speed = self._motor_controllers[0].get()
            return -speed if self._is_inverted else speed
        return 0.0

    def setInverted(self, isInverted: bool = False) -> None:
        self._is_inverted = isInverted

    def getInverted(self) -> bool:
        return self._is_inverted

    def disable(self) -> None:
        for mc in self._motor_controllers:
            mc.disable()

    def stopMotor(self) -> None:
        for mc in self._motor_controllers:
            mc.stopMotor()
