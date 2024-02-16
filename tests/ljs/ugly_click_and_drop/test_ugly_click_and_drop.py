import tkinter
import unittest


class test_ugly_click_and_drop(unittest.TestCase):


    def testClickDrop(self):
        global clicked_card
        clicked_card = None
        global card_count
        card_count = 0
        root = tkinter.Tk()
        root.title("TestTestTest")
        root.geometry("1200x800")
        field = tkinter.Frame(root, width=800, height=400, bg="#000000")
        field.place(relx=0.5, rely=0.3, anchor="center")

        hand = tkinter.Frame(root,width=800, height=200, bg="#AABB00")
        hand.place(relx=0.5, rely=0.8, anchor="center")

        def click(event, _card):
            global clicked_card
            clicked_card = _card
            root.title(f"card: {clicked_card}")

        def drop(event):
            global clicked_card
            global card_count
            card_count += 1
            if clicked_card is not None:

                new_click_card = tkinter.Frame(field, width=100, height=200, bg="#BB00AA")
                new_click_card.place(relx=0.1+ 0.1625*card_count, rely=0.5, anchor="center")
                # clicked_card.place(relx=0.5, rely=0.5, anchor="center")
                # root.title(f"field: {field}, new_click_card: {new_click_card}")
                root.title(f"card_count: {card_count}")
                clicked_card.destroy()
                clicked_card = None


        for i in range(0,5):
            card = tkinter.Frame(hand, width=100, height=200, bg="#BB00AA")
            card.place(relx=0.1+ 0.1625*i, rely=0.5, anchor="center")
            card.bind("<Button-1>", lambda event, _card=card: click(event, _card))


        field.bind("<Button-1>", drop)


        root.mainloop()


if __name__ == '__main__':
    unittest.main()