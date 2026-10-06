from lemonlib import LemonInput


class OI_Base:
    def drive_forward(self) -> float:
        return 0.0

    def drive_turn(self) -> float:
        return 0.0


class Single_OI(OI_Base):
    def __init__(self, port: int):
        self.input1 = LemonInput(0)

    def drive_forward(self) -> float:
        return self.input1.getLeftX()

    def drive_turn(self) -> float:
        return self.input1.getLeftY()
