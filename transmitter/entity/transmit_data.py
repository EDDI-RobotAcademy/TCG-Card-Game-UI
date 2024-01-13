class TransmitData:
    def __init__(self):
        self.__transmit_contents = bytearray(1024)

    def get_transmit_contents(self):
        return self.__transmit_contents
    
