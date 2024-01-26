class PickableRenderer:
    def __init__(self, objects):
        self.objects = objects

    def render(self):
        for obj in self.objects:
            obj.draw()