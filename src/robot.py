from lemonlib.util import curve
from magicbot import MagicRobot
from navx import AHRS
from phoenix5 import WPI_TalonSRX

import oi
from components.drivetrain import Drivetrain


class MyRobot(MagicRobot):
    drivetrain: Drivetrain

    def createObjects(self) -> None:
        self.front_left_motor = WPI_TalonSRX(11)
        self.front_right_motor = WPI_TalonSRX(12)
        self.back_left_motor = WPI_TalonSRX(13)
        self.back_right_motor = WPI_TalonSRX(14)

        self.navx = AHRS.create_spi()

        self.sammi_curve = curve(
            lambda x: 1.89 * x**3 + 0.61 * x, 0.0, deadband=0.1, max_mag=1.0
        )

    def teleopInit(self) -> None:
        self.oi = oi.Single_OI(0)

    def teleopPeriodic(self):
        self.drivetrain.arcade_drive(self.oi.drive_forward(), self.oi.drive_turn())
