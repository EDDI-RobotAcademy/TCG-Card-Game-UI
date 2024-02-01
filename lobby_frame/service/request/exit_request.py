from common.protocol import CustomProtocol


class ExitRequest:
    def __init__(self):
        self.__protocolNumber = CustomProtocol.PROGRAM_EXIT.value

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
        }

    def __str__(self):
        return f"ExitRequest(protocolNumber={self.__protocolNumber})"