

class BattleFieldTimerRepository:
    __instance = None

    timer = 60
    function = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def set_timer(self, setTimer):
        self.timer = setTimer

    def set_function(self, function):
        self.function = function

    def get_timer(self):
        return self.timer

    def get_function(self):
        return self.function

    def clear_every_resource(self):
        self.timer = 60
