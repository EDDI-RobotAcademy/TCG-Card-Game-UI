class AccountRegisterRequest:
    def __init__(self, userId, password):
        self.__userId = userId
        self.__password = password

    def __str__(self):
        return f"AccountRegisterRequest(userId={self.__userId}, password={self.__password})"
