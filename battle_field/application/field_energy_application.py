from battle_field.infra.request.request_attach_field_energy_to_unit import RequestAttachFieldEnergyToUnit
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from session.repository.session_repository_impl import SessionRepositoryImpl


class FieldEnergyApplication:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__session_repository = SessionRepositoryImpl.getInstance()
            cls.__instance.__field_energy_repository = YourFieldEnergyRepository.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def send_request_to_attach_field_energy_to_unit(self, unitIndex, energyRace, energyCount):
        response = self.__field_energy_repository.request_to_attach_energy_to_unit(
            RequestAttachFieldEnergyToUnit(
                #todo : faketest 종료 시 변경 할 필요가 있음
                _sessionInfo=self.__session_repository.get_session_info(),
                # _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                _unitIndex=unitIndex,
                _energyRace=energyRace,
                _energyCount=energyCount
            )
        )
        print(f"send_request_to_attach_field_energy_to_unit response: {response}")
        return response["is_success"]



