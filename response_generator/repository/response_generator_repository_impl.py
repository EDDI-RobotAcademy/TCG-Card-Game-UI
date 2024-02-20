import json

from response_generator.entity.response_generation import ResponseGeneration
from response_generator.repository.response_generator_repository import ResponseGeneratorRepository


class ResponseGeneratorRepositoryImpl(ResponseGeneratorRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def generate_response(self, decodedData):
        print("ResponseGeneratorRepositoryImpl: generate_response()")
        data_dict = json.loads(decodedData)

        for response_type in ResponseGeneration:
            if response_type.name in data_dict:
                response_data = data_dict[response_type.name]
                return response_data

        raise ValueError("Invalid or unsupported response type in the received data")



