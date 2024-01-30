from enum import Enum

class BuyCheckFrame(Enum):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
