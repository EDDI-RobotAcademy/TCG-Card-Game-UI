
from OpenGL import GL


class BattleFieldFrameRenderer:
    def __init__(self, battle_field_scene, window):
        self.battle_field_scene = battle_field_scene
        self.window = window

    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        battle_field_panel_list = self.battle_field_scene.get_battle_field_panel()
        for battle_field_panel in battle_field_panel_list:
            battle_field_panel_shapes = battle_field_panel.get_battle_field_panel_shapes()
            for shape in battle_field_panel_shapes:
                self._render_shape(shape)

        field_list = self.battle_field_scene.get_pickable_field_base()
        for field in field_list:
            field_shapes = field.get_field_shapes()
            for shape in field_shapes:
                self._render_shape(shape)

        # unit_card_list = self.battle_field_scene.get_unit_card()
        # for unit_card in unit_card_list:
        #     unit_shapes = unit_card.get_unit_shapes()
        #     for shape in unit_shapes:
        #         self._render_shape(shape)

        # card_list = self.battle_field_scene.get_pickable_card_base()
        # print(f"card_list: {card_list}")
        # for card in card_list:
        #     card_shapes = card.get_card_shapes()
        #     for shape in card_shapes:
        #         self._render_shape(shape)

        tomb_list = self.battle_field_scene.get_tomb()
        for tomb in tomb_list:
            tomb_shapes = tomb.get_tomb_shapes()
            for shape in tomb_shapes:
                self._render_shape(shape)

        card_deck_list = self.battle_field_scene.get_card_deck()
        for card_deck in card_deck_list:
            card_deck_shapes = card_deck.get_card_deck_shapes()
            for shape in card_deck_shapes:
                self._render_shape(shape)

        trap_list = self.battle_field_scene.get_trap()
        for trap in trap_list:
            trap_shapes = trap.get_trap_shapes()
            for shape in trap_shapes:
                self._render_shape(shape)

        lost_zone_list = self.battle_field_scene.get_lost_zone()
        for lost_zone in lost_zone_list:
            lost_zone_shapes = lost_zone.get_lost_zone_shapes()
            for shape in lost_zone_shapes:
                self._render_shape(shape)

        environment_list = self.battle_field_scene.get_environment()
        for environment in environment_list:
            environment_shapes = environment.get_environment_shapes()
            for shape in environment_shapes:
                self._render_shape(shape)

        energy_field_list = self.battle_field_scene.get_energy_field()
        for energy_field in energy_field_list:
            energy_field_shapes = energy_field.get_energy_field_shapes()
            for shape in energy_field_shapes:
                self._render_shape(shape)

        main_character_list = self.battle_field_scene.get_main_character()
        for main_character in main_character_list:
            main_character_shapes = main_character.get_main_character_shapes()
            for shape in main_character_shapes:
                self._render_shape(shape)

        hand_deck_panel_list = self.battle_field_scene.get_pickable_hand_deck_panel_base()
        for hand_deck_panel in hand_deck_panel_list:
            hand_deck_shapes = hand_deck_panel.get_pickable_hand_deck_panel_shapes()
            for shape in hand_deck_shapes:
                self._render_shape(shape)

        hand_deck_card_list = self.battle_field_scene.get_pickable_hand_deck_card_base()
        for hand_deck_card in hand_deck_card_list:
            hand_deck_card_shapes = hand_deck_card.get_get_pickable_hand_deck_card_base_shapes()
            for shape in hand_deck_card_shapes:
                self._render_shape(shape)

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()