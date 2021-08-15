import tkinter as tk


class GuiTk(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.text = tk.Text(self, state=tk.DISABLED, height=10)
        self.entry = tk.Entry(self)
        self.entry_auxiliary = tk.Entry(self)
        self.read_mode = True

        # self.text.pack(fill=tk.X)
        # self.entry.pack(fill=tk.X, expand=True)
        self.text.grid(row=0, column=1, sticky="nesw")
        self.entry.grid(row=1, column=1, sticky="nesw")

        self.set_read_mode(True)

        parent.bind("<Tab>", self.toggle_mode)

    def toggle_mode(self, *args, **kwargs):
        self.read_mode = not self.read_mode
        self.set_read_mode(self.read_mode)

    def set_read_mode(self, f):
        print(f)
        if not f:
            self.entry_auxiliary.grid(row=2, column=1, sticky="news")
            self.update()
            self.entry_auxiliary.focus_set()
        else:
            self.entry_auxiliary.grid_remove()
            self.entry.focus_set()
            self.update()


if __name__ == "__main__":
    root = tk.Tk()
    gui_tk = GuiTk(root)
    gui_tk.pack(fill=tk.BOTH, expand=True)
    gui_tk.place()
    root.mainloop()

