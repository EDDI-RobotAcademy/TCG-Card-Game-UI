import json
import time
import socket

from colorama import Fore, Style

from receiver.repository.receiver_repository import ReceiverRepository
from response_generator.repository.response_generator_repository_impl import ResponseGeneratorRepositoryImpl


class ReceiverRepositoryImpl(ReceiverRepository):
    __instance = None
    __uiIpcChannel = None
    __clientSocket = None
    __noWaitIpcChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __blockToAcquireSocket(self):
        if self.__clientSocket is None:
            return True

        return False

    def saveClientSocket(self, clientSocket):
        print("ReceiverRepositoryImpl: saveClientSocket()")
        self.__clientSocket = clientSocket

    def saveUiIpcChannel(self, uiIpcChannel):
        print("TransmitterRepositoryImpl: saveIpcChannel()")
        self.__uiIpcChannel = uiIpcChannel

    def saveUiNoWaitIpcChannel(self, noWaitIpcChannel):
        print("TransmitterRepositoryImpl: saveUiNoWaitIpcChannel()")
        self.__noWaitIpcChannel = noWaitIpcChannel

    def receiveCommand(self):
        print("ReceiverRepositoryImpl: receiveCommand()")

        responseGeneratorRepository = ResponseGeneratorRepositoryImpl.getInstance()

        while self.__blockToAcquireSocket():
            time.sleep(0.5)

        socketObject = self.__clientSocket.getSocket()

        while True:
            try:
                data = socketObject.recv(1024)

                if not data:
                    socketObject.close()
                    break

                decodedData = data.decode()
                print(f"{Fore.RED}수신된 정보:{Fore.GREEN} {decodedData}{Style.RESET_ALL}")

                responseData = responseGeneratorRepository.generate_response(decodedData)
                self.__noWaitIpcChannel.put(responseData)
                self.__uiIpcChannel.put(responseData)

                try:
                    json_data = json.loads(decodedData)

                    if "PROGRAM_EXIT" in json_data:
                        print("프로그램 종료 감지")
                        break

                except json.JSONDecodeError as e:
                    print(f"Failed to decode JSON: {e}")

            except (socket.error, BrokenPipeError) as exception:
                print(f"{Fore.RED}사용자 연결 종료{Style.RESET_ALL}")
                return None

            except socket.error as exception:
                print(f"{Fore.RED}전송 중 에러 발생: {Fore.YELLOW}str{exception}{Style.RESET_ALL}")

            except Exception as exception:
                print(f"{Fore.RED}receiver: {Fore.YELLOW}{str(exception)}{Style.RESET_ALL}")

            finally:
                time.sleep(0.5)

        print("Receiver 종료")



