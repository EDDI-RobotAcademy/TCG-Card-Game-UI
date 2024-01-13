from common.protocol import CustomProtocol


class AccountRegisterRequest:
    def __init__(self, userId, password):
        self.__protocolNumber = CustomProtocol.ACCOUNT_REGISTER.value
        self.__userId = userId
        self.__password = password

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "userId": self.__userId,
            "password": self.__password
        }

    def __str__(self):
        return f"AccountRegisterRequest(protocolNumber={self.__protocolNumber}, userId={self.__userId}, password={self.__password})"
