from __future__ import annotations

from dataclasses import dataclass

from phoenix5 import NeutralMode, TalonSRX


@dataclass(frozen=True)
class MotorConfig:
    """
    A default, changable configuration for a single motor controller.

    Attributes:
        inverted: Whether to invert the motor.
        neutral_mode: The mode determining how the motor will behave upon not being commanded voltage.
        reset_to_factory_default: Whether or not to reset all configurations upon initialization.
    """
    inverted: bool = False
    neutral_mode: NeutralMode = NeutralMode.Brake
    reset_to_factory_default: bool = True

    def apply(self, motor: TalonSRX) -> None:
        """
        Applies this configuration to a TalonSRX motor controller.
        """
        if self.reset_to_factory_default:
            motor.configFactoryDefault()

        motor.setInverted(self.inverted)
        motor.setNeutralMode(self.neutral_mode)
