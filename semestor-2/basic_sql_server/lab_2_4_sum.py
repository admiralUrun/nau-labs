import customtkinter as ctk
from tkinter import ttk
import mysql.connector

class TovarApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Сортування за полем")
        self.geometry("650x520")

        # Set light theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Connect to MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1",
            database="market"
        )
        self.cursor = self.conn.cursor()

        self.radio_var = ctk.StringVar(value="price")

        ctk.CTkLabel(self, text="Сортування за:").pack(pady=(10, 0))
        ctk.CTkRadioButton(self, text="Ціна", variable=self.radio_var, value="price", command=self.on_sort).pack()
        ctk.CTkRadioButton(self, text="Кількість", variable=self.radio_var, value="kolichestvo", command=self.on_sort).pack()

        # Table frame
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(pady=10, fill="both", expand=True)

        # Treeview setup
        self.tree = ttk.Treeview(table_frame, columns=("name", "price", "kolichestvo", "sum"), show="headings", height=10)
        self.tree.heading("name", text="Назва")
        self.tree.heading("price", text="Ціна")
        self.tree.heading("kolichestvo", text="Кількість")
        self.tree.heading("sum", text="Сума")

        self.tree.column("name", anchor="w", width=200)
        self.tree.column("price", anchor="center", width=100)
        self.tree.column("kolichestvo", anchor="center", width=100)
        self.tree.column("sum", anchor="center", width=100)

        self.tree.pack(fill="both", expand=True)

        # Label for total count sum
        self.sum_label = ctk.CTkLabel(self, text="Сума кількості: 0.00")
        self.sum_label.pack(pady=10)

        self.on_sort()

    def on_sort(self):
        sort_field = self.radio_var.get()
        query = f"""
            SELECT Tovar.name, price, kolichestvo, price * kolichestvo AS total
            FROM Tovar
            ORDER BY {sort_field} {'ASC' if sort_field == 'price' else 'DESC'}
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

        self.calc_sum()

    def calc_sum(self):
        self.cursor.execute("SELECT SUM(kolichestvo) FROM Tovar")
        total = self.cursor.fetchone()[0] or 0.0
        self.sum_label.configure(text=f"Сума кількості: {total:.2f}")

if __name__ == "__main__":
    app = TovarApp()
    app.mainloop()
