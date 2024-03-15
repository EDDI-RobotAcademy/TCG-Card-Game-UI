class EffectAnimationRepository:
    __instance = None
    __effect_animation_list = []
    __effect_animation_panel_list = []
    __effect_animation_dictionary = {}
    __effect_animation_panel_dictionary = {}
    __is_animation_playing = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_effect_animation_list(self):
        return self.__effect_animation_list

    def get_effect_animation_panel_list(self):
        return self.__effect_animation_panel_list

    def reset_all_effect_animation(self):
        self.__effect_animation_list = []
        self.__effect_animation_panel_list = []

    def save_effect_animation_at_dictionary_with_index(self, index, effect_animation):
        print(index)
        print(effect_animation)
        self.__effect_animation_dictionary[index] = effect_animation

    def save_effect_animation_at_dictionary_without_index_and_return_index(self, effect_animation):
        index = 1000
        while True:
            if index in self.__effect_animation_dictionary.keys():
                index += 1
            else:
                self.__effect_animation_dictionary[index] = effect_animation
                return index

    def get_effect_animation_by_index(self, index):
        return self.__effect_animation_dictionary[index]

    def save_effect_animation_panel_at_dictionary_with_index(self, index, effect_animation_panel):
        print(index)
        print(effect_animation_panel)
        self.__effect_animation_panel_dictionary[index] = effect_animation_panel


    def get_effect_animation_panel_by_index(self, index):
        return self.__effect_animation_panel_dictionary[index]

    def remove_effect_animation_by_index(self, index):
        del self.__effect_animation_panel_dictionary[index]
        del self.__effect_animation_dictionary[index]

    def get_effect_animation_dictionary(self):
        return self.__effect_animation_dictionary

    def get_effect_animation_panel_dictionary(self):
        return self.__effect_animation_panel_dictionary

    def clear_every_resource(self):
        self.__effect_animation_list = []
        self.__effect_animation_panel_list = []
        self.__effect_animation_dictionary = {}
        self.__effect_animation_panel_dictionary = {}
        self.__is_animation_playing = False
