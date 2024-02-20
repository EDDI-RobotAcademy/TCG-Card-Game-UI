from image_shape.circle_image import CircleImage
from image_shape.circle_number_image import CircleNumberImage
from opengl_battle_field_pickable_card.pickable_card import PickableCard


class LocationInitializer:
    @staticmethod
    def return_to_initial_location(selected_object):
        if not isinstance(selected_object, PickableCard):
            return

        pickable_card_base = selected_object.get_pickable_card_base()
        initial_vertices = pickable_card_base.get_initial_vertices()
        pickable_card_base.update_vertices(initial_vertices)

        tool_card = selected_object.get_tool_card()
        if tool_card is not None:
            tool_initial_vertices = tool_card.get_initial_vertices()
            tool_card.update_vertices(tool_initial_vertices)

        for attached_shape in pickable_card_base.get_attached_shapes():
            if isinstance(attached_shape, CircleImage) or isinstance(attached_shape, CircleNumberImage):
                initial_center = attached_shape.get_initial_center()
                attached_shape.update_circle_vertices(initial_center)
            else:
                initial_vertices = attached_shape.get_initial_vertices()
                attached_shape.update_vertices(initial_vertices)
