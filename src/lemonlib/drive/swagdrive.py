from wpilib.drive import DifferentialDrive
from wpilib.interfaces._interfaces import MotorController

from lemonlib.smart.preference import SmartPreference


class SwagDrive:
    def __init__(self, leftMotor: MotorController, rightMotor: MotorController) -> None:
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor
        self.robotDrive = DifferentialDrive(self.leftMotor, self.rightMotor)

        self.maxspeed = SmartPreference("Swag/MaxSpeed", 0.8)
        self.defspeed = SmartPreference("Swag/DefSpeed", 0.5)
        self.swagadd = SmartPreference("Swag/SwagAdd", 1)
        self.maxswag = SmartPreference("Swag/MaxSwag", 9000)
        self.minswag = SmartPreference("Swag/MinSwag", 0.1)
        self.swagmulti = SmartPreference("Swag/SwagMulti", 10)

        # Swag-related variables
        self.swagLevel = 0
        self.swagPeriod = 0
        self.oldMove = 0
        self.oldRotate = 0

    def Drive(self, moveValue: float, rotateValue: float):
        """Custom drive function that incorporates 'swag' logic."""

        SWAG_BARRIER = self.minswag
        SWAG_MULTIPLIER = self.swagmulti
        MAX_SWAG_LEVEL = self.maxswag
        SWAG_PERIOD = 500
        SWAG_ADD = self.swagadd

        moveToSend = moveValue
        rotateToSend = rotateValue
        moveDiff = abs(moveValue - self.oldMove)
        rotateDiff = abs(rotateValue - self.oldRotate)

        if self.swagPeriod == 0:
            if moveDiff < SWAG_BARRIER.get():
                moveToSend = (moveDiff * SWAG_MULTIPLIER.get()) + moveValue
            else:
                self.swagLevel += SWAG_ADD.get()

            if rotateDiff < SWAG_BARRIER.get():
                rotateToSend = (rotateDiff * SWAG_MULTIPLIER.get()) + rotateValue
            else:
                self.swagLevel += SWAG_ADD.get()

            if self.swagLevel > MAX_SWAG_LEVEL.get():
                self.swagPeriod = SWAG_PERIOD
                self.swagLevel = 0

        else:
            moveToSend = 0
            rotateToSend = 1.0
            self.swagPeriod -= 1

        self.rotatediff = rotateDiff
        self.movediff = moveDiff
        # Call arcadeDrive with modified move and rotate values
        self.robotDrive.arcadeDrive(moveToSend, rotateToSend)

        self.oldMove = moveValue
        self.oldRotate = rotateValue
