class DetectorAboutTest:
    __instance = None

    is_it_test = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def set_is_it_test(self, is_it_test):
        self.is_it_test = is_it_test

    def get_is_it_test(self):
        return self.is_it_test
