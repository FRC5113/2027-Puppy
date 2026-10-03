from __future__ import annotations

from typing import final

from wpilib import TimedRobot

from mode_robot.modes.base import Mode
from mode_robot.modes.teleop_mode import TeleopMode
from mode_robot.modes.autonomous_mode import AutonomousMode
from mode_robot.modes.disabled_mode import DisabledMode
from mode_robot.modes.test_mode import TestMode


class ModeRobot(TimedRobot):
    """
    A simple framework that allows for modes to be encapsulated in their own files.
    This is conceptially very similar to `OpModeRobot`; however, it internally
    inherits from the `TimedRobot` framework to be compatible with the 2026
    version of wpilib.

    Usage:
        - None of the default lifecycle methods (i.e. `testPeriodic`, `autonomousInit`) may be overriden.
        - For robot-wide behavior, override the `robot_init` and `robot_periodic` methods.
    """
    def __init__(
        self, 
        teleop_mode: TeleopMode,
        autonomous_mode: AutonomousMode,
        disabled_mode: DisabledMode,
        test_mode: TestMode,
        period: float = 0.02,
    ) -> None:
        """
        Initializes `ModeRobot`.
        
        Args:
            period: The period for the robot. This dictates how often the periodic
                    hooks in each mode will be executed. Defaults to 0.02s (50Hz).
        """
        super().__init__(period)

        self._active_mode: Mode | None = None
        self._teleop_mode = teleop_mode
        self._autonomous_mode = autonomous_mode
        self._disabled_mode = disabled_mode
        self._test_mode = test_mode

    def _enter_mode(self, mode: Mode) -> None:
        """
        Sets the internal mode for the class & runs the entered method.
        """
        self._active_mode = mode
        self._active_mode.on_enter()

    def _exit_mode(self) -> None:
        """
        Resets the current mode to `None` & runs the exited method.
        """
        if self._active_mode is not None:
            self._active_mode.on_exit()
        self._active_mode = None

    def _run_mode_periodic(self) -> None:
        """
        Calls the periodic method for the mode (assuming the mode is not None).
        """
        if self._active_mode is not None:
            self._active_mode.on_periodic()

    @final
    def robotInit(self) -> None:
        """
        Do not override this method.
        
        Calls the `robot_init` method upon the robot being initialized.
        """
        self.robot_init()

    @final
    def robotPeriodic(self) -> None:
        """
        Do not override this method.
        
        Calls the `robot_periodic` method each iteration.
        """
        self.robot_periodic()

    @final
    def autonomousInit(self) -> None:
        """
        Do not override this method.
        
        Sets the current internal mode to autonomous.
        """
        self._enter_mode(self._autonomous_mode)

    @final
    def autonomousPeriodic(self) -> None:
        """
        Do not override this method.
        
        Calls the periodic method to the current autonomous mode.
        """
        self._run_mode_periodic()

    @final
    def autonomousExit(self) -> None:
        """
        Do not override this method.
        
        Sets the current internal mode to None.
        """
        self._exit_mode()

    @final
    def teleopInit(self) -> None:
        """
        Do not override this method.

        Sets the current internal mode to the teleoperated mode.
        """
        self._enter_mode(self._teleop_mode)

    @final
    def teleopPeriodic(self) -> None:
        """
        Do not override this method.

        Calls the periodic method of the current teleoperated mode.
        """
        self._run_mode_periodic()

    @final
    def teleopExit(self) -> None:
        """
        Do not override this method.

        Clears the current internal mode after teleoperated mode ends.
        """
        self._exit_mode()

    @final
    def disabledInit(self) -> None:
        """
        Do not override this method.

        Sets the current internal mode to the disabled mode.
        """
        self._enter_mode(self._disabled_mode)

    @final
    def disabledPeriodic(self) -> None:
        """
        Do not override this method.

        Calls the periodic method of the current disabled mode.
        """
        self._run_mode_periodic()

    @final
    def disabledExit(self) -> None:
        """
        Do not override this method.

        Clears the current internal mode after disabled mode ends.
        """
        self._exit_mode()

    @final
    def testInit(self) -> None:
        """
        Do not override this method.

        Sets the current internal mode to the test mode.
        """
        self._enter_mode(self._test_mode)

    @final
    def testPeriodic(self) -> None:
        """
        Do not override this method.

        Calls the periodic method of the current test mode.
        """
        self._run_mode_periodic()

    @final
    def testExit(self) -> None:
        """
        Do not override this method.

        Clears the current internal mode after test mode ends.
        """
        self._exit_mode()

    def robot_init(self) -> None:
        """
        Called once upon the robot being enabled.
        
        All robot-wide initialization (not specific to an opmode) should go here.
        """
        pass

    def robot_periodic(self) -> None:
        """
        Called every iteration upon the robot being enabled.
        
        All robot-wide processes (not specific to an opmode) should go here.
        """
        pass
