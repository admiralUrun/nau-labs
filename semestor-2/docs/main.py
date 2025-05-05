import os

import customtkinter as ctk
import webbrowser

ctk.set_appearance_mode("light")

class HelpApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TestHelp")
        self.geometry("400x350")

        # Entry A
        self.label_a = ctk.CTkLabel(self, text="A:")
        self.label_a.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_a = ctk.CTkEntry(self)
        self.entry_a.grid(row=0, column=1, padx=10, pady=5)

        # Entry B
        self.label_b = ctk.CTkLabel(self, text="B:")
        self.label_b.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_b = ctk.CTkEntry(self)
        self.entry_b.grid(row=1, column=1, padx=10, pady=5)

        # Combobox
        self.combobox = ctk.CTkComboBox(self, values=["+", "-", "*", "/"])
        self.combobox.grid(row=2, column=0, columnspan=2, pady=10)
        self.combobox.set("+")

        # Buttons
        self.button_ok = ctk.CTkButton(self, text="OK", command=self.calculate)
        self.button_ok.grid(row=3, column=0, pady=10)

        self.button_clear = ctk.CTkButton(self, text="Clear", command=self.clear_log)
        self.button_clear.grid(row=3, column=1, pady=10)

        # Memo
        self.memo = ctk.CTkTextbox(self, height=100)
        self.memo.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

        # Help button (bottom right)
        self.help_button = ctk.CTkButton(self, text="Довідка", command=self.open_main_doc, width=80)
        self.help_button.grid(row=5, column=1, sticky="e", padx=10, pady=(0, 10))

        # F1 key binding
        self.bind_all("<F1>", self.open_help)

        # Help context mapping
        self.help_contexts = {
            self.entry_a: "edit.html",
            self.entry_b: "edit.html",
            self.combobox: "combobox.html",
            self.button_ok: "button.html",
            self.memo: "memo.html",
        }

    def calculate(self):
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            op = self.combobox.get()
            if op == "/" and b == 0:
                raise ZeroDivisionError("Ділення на нуль")
            result = eval(f"{a} {op} {b}")
            self.memo.insert("end", f"{a:.2f} {op} {b:.2f} = {result:.2f}\n")
        except Exception as e:
            self.memo.insert("end", f"Помилка: {e}\n")

    def clear_log(self):
        self.memo.delete("1.0", "end")

    def open_help(self, event):
        widget = self.focus_get()
        file = self.help_contexts.get(widget)
        if file:
            path = os.path.abspath(f"semestor-2/docs/help_docs/{file}")
            webbrowser.open(f"file://{path}")

    def open_main_doc(self):
        path = os.path.abspath("semestor-2/docs/help_docs/index.html")
        print("Відкриваємо:", path)
        webbrowser.open(f"file://{path}")

if __name__ == "__main__":
    app = HelpApp()
    app.mainloop()
