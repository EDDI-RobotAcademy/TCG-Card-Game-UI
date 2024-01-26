import tkinter


class Timer(tkinter.Label):
    __max_time = None
    __timer_id = None
    __remain_time = None
    __expired_event = None


    def __init__(self, rootWindow, time, relx, rely, expiredEvent):
        super().__init__(rootWindow, text=str(time), font=("Helvetica", 30, "bold"), fg="#FF0000", bg="#000000")
        self.place(relx=relx, rely=rely, anchor="center")
        self.__max_time = time
        self.__expired_event = expiredEvent

    def startTimer(self):
        if self.__timer_id is None:
            self.updateTimer()

    def resetTimer(self):
        self.__remain_time = self.__max_time
        self.__timer_id = None

    def updateTimer(self):
        self.configure(text=str(self.__remain_time))

        if self.__remain_time >= 0:
            self.__remain_time -= 1
            self.__timer_id = self.master.after(1000, self.updateTimer)
        else:
            self.__expired_event()

    def editTimer(self, _newTime, _newEvent=None):
        self.__remain_time = _newTime
        if _newEvent:
            self.__expired_event = _newEvent

    def deleteTimer(self):
        self.destroy()