import tkinter

from my_card_frame.repository.my_card_frame_repository_impl import MyCardFrameRepositoryImpl
from my_card_frame.service.my_card_frame_service import MyCardFrameService
from my_deck_frame.service.my_deck_frame_service_impl import MyDeckFrameRepositoryImpl, MyDeckFrameServiceImpl


class MyCardFrameServiceImpl(MyCardFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__myCardFrameRepository = MyCardFrameRepositoryImpl.getInstance()
            cls.__instance.__myDeckFrameRepository = MyDeckFrameRepositoryImpl.getInstance()
            cls.__instance.__myDeckFrameService = MyDeckFrameServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def createMyCardUiFrame(self, rootWindow):
        myCardFrame = self.__myCardFrameRepository.createMyCardFrame(rootWindow)

        label_text = "My Card"
        label = tkinter.Label(myCardFrame, text=label_text, font=("Helvetica", 40), bg="black", fg="white",
                               anchor="center", justify="center", pady=200)

        label.place(relx=0.3, rely=0.2, anchor="center", bordermode="outside")  # 가운데 정렬


        #MyCardFrame 위에 MyDeckFrame 띄우기
        myDeckFrame = self.__myDeckFrameService.createMyDeckUiFrame(myCardFrame, myCardFrame)
        myDeckFrame.pack(side="right", expand=False)


        return myCardFrame
