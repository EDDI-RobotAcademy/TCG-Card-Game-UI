from common.protocol import CustomProtocol


class ProgramExitRequest:
    def __init__(self):
        self.__protocolNumber = CustomProtocol.PROGRAM_EXIT.value

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
        }

    def __str__(self):
        return f"ProgramExitRequest(protocolNumber={self.__protocolNumber})"
