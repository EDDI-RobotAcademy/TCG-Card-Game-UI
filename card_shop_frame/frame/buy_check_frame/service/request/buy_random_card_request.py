from common.protocol import CustomProtocol


class BuyRandomCardRequest:
    def __init__(self, sessionInfo, race_name, is_confirmed_upper_legend):
        self.__protocolNumber = CustomProtocol.SHOP_GACHA.value
        self.__sessionInfo = sessionInfo
        self.__race_name = race_name
        self.__is_confirmed_upper_legend = is_confirmed_upper_legend

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "race_name": self.__race_name,
            "is_confirmed_upper_legend": self.__is_confirmed_upper_legend
        }

    def __str__(self):
        return (f"BuyRandomCardRequest(protocolNumber={self.__protocolNumber},sessionInfo={self.__sessionInfo}, race_name={self.__race_name},is_confirmed_upper_legend={self.__is_confirmed_upper_legend})")
