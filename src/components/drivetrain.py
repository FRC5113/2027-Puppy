from lemonlib.util.motor_controller_group import MotorControllerGroup
from magicbot import feedback, will_reset_to
from navx import AHRS
from phoenix5 import WPI_TalonSRX
from wpilib import SmartDashboard
from wpilib.drive import DifferentialDrive


class Drivetrain:
    front_left_motor: WPI_TalonSRX
    front_right_motor: WPI_TalonSRX
    back_left_motor: WPI_TalonSRX
    back_right_motor: WPI_TalonSRX

    navx: AHRS

    forward = will_reset_to(0.0)
    turn = will_reset_to(0.0)

    def setup(self):
        self.right_motor = MotorControllerGroup(
            self.front_right_motor, self.back_right_motor
        )
        self.left_motor = MotorControllerGroup(
            self.front_left_motor, self.back_left_motor
        )

        self.drive = DifferentialDrive(self.left_motor, self.right_motor)

        SmartDashboard.putData(self.drive)

    @feedback
    def get_angle(self):
        return self.navx.getYaw()

    def arcade_drive(self, forward: float, turn: float):
        self.forward = forward
        self.turn = turn

    def execute(self):
        self.drive.arcadeDrive(self.forward, self.turn)
