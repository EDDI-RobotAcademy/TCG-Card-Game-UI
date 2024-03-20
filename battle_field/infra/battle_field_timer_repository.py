

class BattleFieldTimerRepository:
    __instance = None

    timer = 60
    function = None
    unit_timer = 10
    unit_timeout_function = None

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

    def set_unit_timer(self, unitTimer):
        print("유닛 타이머 설정")
        self.unit_timer = unitTimer

    def set_unit_timeout_function(self, unitTimeoutFunction):
        self.unit_timeout_function = unitTimeoutFunction

    def get_timer(self):
        return self.timer

    def get_function(self):
        return self.function

    def get_unit_timer(self):
        return self.unit_timer

    def get_unit_timeout_function(self):
        return self.unit_timeout_function

    def clear_every_resource(self):
        self.timer = 60
        self.function = None
