class PickingCardFrameRenderer:
    def __init__(self, unit_card_list, window):
        self.unit_card_list = unit_card_list
        self.window = window

    def render(self):
        self.window.tkMakeCurrent()

        for unit_card in self.unit_card_list:
            pickable_unit_card_base = unit_card.get_pickable_unit_card_base()
            attached_tool_card = unit_card.get_tool_card()
            attached_shape_list = pickable_unit_card_base.get_attached_shapes()

            attached_tool_card.draw()

            for attached_shape in attached_shape_list:
                attached_shape.draw()

        self.window.tkSwapBuffers()

    # def on_canvas_drag(self, event):
    #     print(f"on_canvas_drag x: {event.x}, y: {event}")
    #     x, y = event.x, event.y
    #     y = self.window.winfo_reqheight() - y
    #
    #     if self.window.selected_object and self.window.drag_start:
    #         print(f"selected_object: {self.window.selected_object}")
    #         for object_shapes in self.selected_object.get_object_shapes():
    #             print(f"object_shapes: {object_shapes}")
    #             dx = x - self.drag_start[0]
    #             dy = y - self.drag_start[1]
    #
    #             new_vertices = [
    #                 (vx + dx, vy + dy) for vx, vy in object_shapes.vertices
    #             ]
    #
    #             object_shapes.update_vertices(new_vertices)
    #
    #             attached_shape_list = object_shapes.get_attached_shapes()
    #             for attached_shape in attached_shape_list:
    #                 attached_shape.update_vertices(new_vertices)
    #
    #             self.window.drag_start = (x, y)
    #             self.render()
    #
    # def on_canvas_release(self, event):
    #     self.window.drag_start = None
    #
    # def on_canvas_click(self, event):
    #     print(f"on_canvas_click: {event}")
    #     try:
    #         x, y = event.x, event.y
    #         y = self.window.winfo_reqheight() - y
    #
    #         for unit_card in self.unit_card_list:
    #             print(f"type(unit_card): {type(unit_card)}")
    #             if isinstance(unit_card, UnitCard):
    #                 unit_card.selected = False
    #
    #         self.selected_object = None
    #
    #         # for unit_card in reversed(self.unit_card_list):
    #         #     pickable_unit_card_base = unit_card.get_pickable_unit_card_base()
    #         #     attached_shape_list = pickable_unit_card_base.get_attached_shapes()
    #         #     for shape in attached_shape_list:
    #         #         if isinstance(shape, PickableRectangle) and shape.is_point_inside((x, y)):
    #         #             pickable_unit_card_base.selected = not pickable_unit_card_base.selected
    #         #             self.selected_object = pickable_unit_card_base
    #         #             self.drag_start = (x, y)
    #         #             print(f"Selected PickableRectangle at ({x}, {y})")
    #         #             break
    #
    #         self.render()
    #     except Exception as e:
    #         print(f"Exception in on_canvas_click: {e}")