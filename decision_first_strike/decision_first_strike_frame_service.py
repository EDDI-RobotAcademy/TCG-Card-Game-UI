import tkinter

from decision_first_strike.entity.DecisionFirstStrikeFrame import DecisionFirstStrikeFrame


class DecisionFirstStrikeFrameService:
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



    def create_decision_first_strike_frame(self, rootWindow, switchFrameWithMenuName):
        decision_first_strike_frame = DecisionFirstStrikeFrame(rootWindow)

        next_button = tkinter.Button(decision_first_strike_frame, text="확인")
        next_button.place(relx=0.5, rely=0.5, anchor="center")

        def to_next_frame(event):
            switchFrameWithMenuName('battle-field')

        next_button.bind("<Button-1>", to_next_frame)

        return decision_first_strike_frame

