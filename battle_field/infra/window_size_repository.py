class WindowSizeRepository:
    __instance = None

    total_width = None
    total_height = None
    is_it_re_entrance = False
    master_opengl_frame = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def get_total_width(self):
        return self.total_width

    def get_total_height(self):
        return self.total_height

    def set_is_it_re_entrance(self, is_it_re_entrance):
        self.is_it_re_entrance = is_it_re_entrance

    def get_is_it_re_entrance(self):
        return self.is_it_re_entrance

    def set_master_opengl_frame(self, master_opengl_frame):
        self.master_opengl_frame = master_opengl_frame

    def get_master_opengl_frame(self):
        return self.master_opengl_frame
