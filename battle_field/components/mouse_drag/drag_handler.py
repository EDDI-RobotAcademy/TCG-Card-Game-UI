from opengl_battle_field_pickable_card.pickable_card import LegacyPickableCard


class DragHandler:
    def __init__(self, selected_object, drag_start):
        self.selected_object = selected_object
        self.drag_start = drag_start

    def update_selected_object_vertices_with_drag(self, dx, dy):
        if not isinstance(self.selected_object, LegacyPickableCard):
            return

        pickable_card = self.selected_object.get_pickable_card_base()

        new_vertices = [
            (vx + dx, vy + dy) for vx, vy in pickable_card.vertices
        ]
        pickable_card.update_vertices(new_vertices)

        tool_card = self.selected_object.get_tool_card()
        if tool_card is not None:
            new_tool_card_vertices = [
                (vx + dx, vy + dy) for vx, vy in tool_card.vertices
            ]
            tool_card.update_vertices(new_tool_card_vertices)

        for attached_shape in pickable_card.get_attached_shapes():
            new_attached_shape_vertices = [
                (vx + dx, vy + dy) for vx, vy in attached_shape.vertices
            ]
            attached_shape.update_vertices(new_attached_shape_vertices)
