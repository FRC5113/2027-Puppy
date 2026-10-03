from __future__ import annotations

from wpilib import XboxController, Field2d, SmartDashboard

from mode_robot import ModeRobot

from puppy.modes.teleop_mode import Teleop
from puppy.modes.test_mode import Test
from puppy.modes.autonomous_mode import Autonomous
from puppy.modes.disabled_mode import Disabled

from puppy.subsystems.drivetrain import Drivetrain
from puppy.subsystems.drivetrain.io import DrivetrainSimIO, DrivetrainRealIO


class Puppy(ModeRobot):
    """
    The main robot orchestrator for robot-wide logic & mode initialization.
    """
    def __init__(self) -> None:
        """
        Initializes all IOs, hardware, and subsystems for the robot.
        """
        self.controller = XboxController(0)

        if self.isSimulation():
            self.drivetrain_io = DrivetrainSimIO()
        else:
            self.drivetrain_io = DrivetrainRealIO()

        self.drivetrain = Drivetrain(self.drivetrain_io)

        self.simulated_field = Field2d()
        SmartDashboard.putData("SimulatedField", self.simulated_field)

        super().__init__(
            teleop_mode=Teleop(self.drivetrain, self.controller),
            autonomous_mode=Autonomous(),
            disabled_mode=Disabled(self.drivetrain),
            test_mode=Test()
        )

    def robot_periodic(self) -> None:
        """
        Updates the state of all subsystems and IOs every iteration, no matter the mode.
        """
        self.drivetrain_io.update()
        self.drivetrain.update()

        pose = self.drivetrain.get_pose()
        if pose is not None:
            self.simulated_field.setRobotPose(pose)
