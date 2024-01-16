import abc


class ResponseGeneratorRepository(abc.ABC):
    @abc.abstractmethod
    def generate_response(self, decodedData):
        pass