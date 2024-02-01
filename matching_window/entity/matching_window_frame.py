import tkinter

from utility.image_generator import ImageGenerator


imageWidth = 256
imageHeight = 256

class MatchingWindowFrame(tkinter.Frame):
    __isMatching = None

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.__imageGenerator = ImageGenerator.getInstance()
        self.configure(width=480, height=360)
        self.place(relx=0.5, rely=0.5, anchor="center")


        self.__matchingText = tkinter.Label(master=self, text="매칭 시작!")
        self.__matchingText.place(relx=0.5, rely=0.1, anchor="center")

        self.__matchingBar = tkinter.Frame(master=self, width=0, height=36, bg="#E22500")
        self.__matchingBar.place(relx=0.5, rely=0.875, anchor="center")

        self.__waitingImage = tkinter.Canvas(master=self, width=imageWidth, height=imageHeight)
        generatedImage = self.__imageGenerator.getRandomCardImage()
        self.__waitingImage.create_image(imageWidth / 2, imageHeight / 2, image=generatedImage)
        self.__waitingImage.place(relx=0.5, rely=0.5, anchor="center", width=imageWidth, height=imageHeight)

        self.__cancelMatchingButton = tkinter.Button(master = self, text="매칭 취소")
        self.__cancelMatchingButton.place(relx=0.5, rely=0.95, anchor="center")

        self.__isMatching = True
        # self.__matchingPercent = tkinter.Label(matchingWindow)
        # self.__matchingPercent.place(relx=0.5, rely=0.96, anchor="center")

    def updateMatchingImage(self):
        generatedImage = self.__imageGenerator.getRandomCardImage()
        self.__waitingImage.create_image(imageWidth / 2, imageHeight / 2, image=generatedImage)

    def updateMatchingBarWidth(self, i, rootWindow):
        if self.__isMatching:
            self.__matchingBar.configure(width=i, height=9)
            if i < 480:
                rootWindow.after(10, lambda: self.updateMatchingBarWidth(i + (480 / 60 / 100), rootWindow))
                # self.__waitingPercent.configure(text=f"{round((i + (480 / 60 / 100)) / 480 * 100)}%")
            else:
                self.destroy()


    def getCancelMatchingButton(self):
        return self.__cancelMatchingButton

    def changeWindowText(self, text):
        self.__matchingText.configure(text=text)

    def hideMatchingUI(self):
        self.__matchingBar.place_forget()
        self.__cancelMatchingButton.place_forget()
        self.__isMatching = False
        #self.__matchingPercent.place_forget()
