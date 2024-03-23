from battle_field_function.service.battle_field_function_service_impl import BattleFieldFunctionServiceImpl
from notify_reader.controller.notify_reader_controller import NotifyReaderController
from notify_reader.service.notify_reader_service_impl import NotifyReaderServiceImpl


class FakeNotifyReaderControllerImpl(NotifyReaderController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__notifyReaderService = NotifyReaderServiceImpl.getInstance()
            cls.__instance.__battleFieldFunctionService = BattleFieldFunctionServiceImpl.getInstance()
            #todo : 실행되어야 할 함수 위치를 등록해주세요
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def requestToMappingNoticeWithFunction(self):
        #todo : 함수를 등록해주세요

        hand_use_function = self.__battleFieldFunctionService.useHandCard
        self.__notifyReaderService.saveHandCardUseFunction(hand_use_function)

        draw_count_function = self.__battleFieldFunctionService.drawOpponentCard
        self.__notifyReaderService.saveDrawCountFunction(draw_count_function)

        drawn_card_list_function = self.__battleFieldFunctionService.drawYourCard
        self.__notifyReaderService.saveDrawnCardListFunction(drawn_card_list_function)

        deck_card_use_list_function = self.__battleFieldFunctionService.useDeckCardList
        self.__notifyReaderService.saveDeckCardUseListFunction(deck_card_use_list_function)

        field_unit_energy_function = self.__battleFieldFunctionService.attachFieldUnitEnergy
        self.__notifyReaderService.saveFieldUnitEnergyFunction(field_unit_energy_function)

        search_count_function = self.__battleFieldFunctionService.searchOpponentCount
        self.__notifyReaderService.saveSearchCountFunction(search_count_function)

        search_card_list_function = self.__battleFieldFunctionService.searchYourCardList
        self.__notifyReaderService.saveSearchCardListFunction(search_card_list_function)

        spawn_unit_function = self.__battleFieldFunctionService.spawnOpponentUnit
        self.__notifyReaderService.saveSpawnUnitFunction(spawn_unit_function)


    def requestToReadNotifyCommand(self):
        self.__notifyReaderService.readNoticeAndCallFunction()

    def requestToInjectNoWaitIpcChannel(self, no_wait_ipc_channel):
        self.__notifyReaderService.injectNoWaitIpcChannel(no_wait_ipc_channel)