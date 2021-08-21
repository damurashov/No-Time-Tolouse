import tkinter as tk
from api import Soimort
from storage import Csv
import re


class GuiTk(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.text = tk.Text(self, height=10, state=tk.DISABLED)
        self.entry = tk.Entry(self)
        self.entry_auxiliary = tk.Entry(self)
        self.read_mode = True

        self.storage = Csv("vocabulary.csv")
        self.api = Soimort()

        # self.text.pack(fill=tk.X)
        # self.entry.pack(fill=tk.X, expand=True)
        self.text.grid(row=0, column=1, sticky="nesw")
        self.entry.grid(row=1, column=1, sticky="nesw")

        self.set_read_mode(True)

        parent.bind("<Tab>", self.toggle_mode)
        self.entry.bind("<Return>", lambda e: self.get_translation())
        self.entry_auxiliary.bind("<Return>", lambda e: self.save_translation())

    def get_translation(self):

        translations = self.api.translate(self.entry.get(), "en", "ru")
        saved_translations = self.storage.find(self.entry.get())

        output = ""
        for pair in saved_translations:
            output = output + (">> " + ' :: '.join(list(pair)) + '\n')
        output = output + '\n'.join(translations) + '\n'

        self.text.configure(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.INSERT, output)
        self.text.configure(state=tk.DISABLED)
        self.update()

    def save_translation(self):
        phrase = self.entry.get()
        translation = self.entry_auxiliary.get()

        re_spaces = r'(^[ \t]+|[ \t]+(?=:))'
        f_phrase_emptry = len(re.sub(re_spaces, '', phrase)) == 0
        f_translation_empty = len(re.sub(re_spaces, '', translation)) == 0

        if not (f_phrase_emptry and f_translation_empty):
            self.storage.write(phrase.strip(), translation.strip())

        self.entry.delete(0, tk.END)
        self.entry_auxiliary.delete(0, tk.END)
        self.set_read_mode(True)

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

