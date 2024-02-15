class PageManager:
    def __init__(self):
        self.current_page = 1

    def go_to_next_page(self):
        self.current_page += 1

    def go_to_previous_page(self):
        self.current_page -= 1

    def get_current_page(self):
        return self.current_page