from opengl_dummy_frame.dummy_frame import DummyFrame


class OpenGLDummyFrameRepository:
    __instance = None
    __dummy_frame = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_dummy_frame(self):
        return self.__dummy_frame

    def createOpenGLDummyFrame(self, rootWindow):
        print("OpenGLDummyFrameRepository: createOpenGLDummyFrame()")
        __dummy_frame = DummyFrame(rootWindow)

        return __dummy_frame
