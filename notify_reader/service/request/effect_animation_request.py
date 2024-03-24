class EffectAnimationRequest:
    def __init__(self, effect_animation, target_player, target_type, target_index, call_function=None, function_need_param = False, param=None, need_dalay = False):
        self.effect_animation = effect_animation
        self.target_player = target_player
        self.target_type = target_type
        self.target_index = target_index
        self.call_function = call_function
        self.function_need_param = function_need_param
        self.param = param
        self.need_delay = need_dalay

    def get_param(self):
        return self.param

    def get_need_delay(self):
        return self.need_delay

    def get_function_need_param(self):
        return self.function_need_param

    def get_effect_animation(self):
        return self.effect_animation

    def get_target_player(self):
        return self.target_player

    def get_target_type(self):
        return self.target_type

    def get_target_index(self):
        return self.target_index

    def get_call_function(self):
        print("call function~~",self.call_function)
        return self.call_function