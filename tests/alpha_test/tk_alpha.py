import tkinter as tk


def main():
    root = tk.Tk()
    # root.attributes('-alpha', 0.3)  # 앱 전체가 투명해짐
    #root.wm_attributes("-transparentcolor", True)  # 흰색을 투명하도록 지정
    root.config(bg='')
    canvas = tk.Canvas(root, width=600, height=300)  # 배경을 흰색으로 지정
    canvas.grid(columnspan=3, rowspan=3)
    instructions = tk.Label(root, text="Hello World", font="Raleway")
    instructions.grid(columnspan=3, column=0, row=0)

    root.mainloop()

if __name__ == "__main__":
    main()
