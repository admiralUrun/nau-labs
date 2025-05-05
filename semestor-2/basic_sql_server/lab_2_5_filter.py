import customtkinter as ctk
from tkinter import ttk
import mysql.connector

class TovarApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Фільтрація по Відділу та Постачальнику")
        self.geometry("700x550")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1",
            database="market"
        )
        self.cursor = self.conn.cursor()

        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(pady=10, fill="x")

        # Відділ
        ctk.CTkLabel(self.filter_frame, text="Відділ:").grid(row=0, column=0, padx=10)
        self.cb_otd = ttk.Combobox(self.filter_frame, state="readonly")
        self.cb_otd.grid(row=0, column=1, padx=5)
        self.cb_otd.bind("<<ComboboxSelected>>", self.on_filter_change)
        self.cb_otd.bind("<Escape>", self.reset_filter)

        # Постачальник
        ctk.CTkLabel(self.filter_frame, text="Постачальник:").grid(row=0, column=2, padx=10)
        self.cb_post = ttk.Combobox(self.filter_frame, state="readonly")
        self.cb_post.grid(row=0, column=3, padx=5)
        self.cb_post.bind("<<ComboboxSelected>>", self.on_filter_change)
        self.cb_post.bind("<Escape>", self.reset_filter)

        # Таблиця
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("name", "price", "kolichestvo", "sum"), show="headings", height=10)
        for col, label, width in zip(("name", "price", "kolichestvo", "sum"),
                                     ("Назва", "Ціна", "Кількість", "Сума"),
                                     (200, 100, 100, 100)):
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.sum_label = ctk.CTkLabel(self, text="Сума кількості: 0.00")
        self.sum_label.pack(pady=10)

        self.load_filters()
        self.on_filter_change()

    def load_filters(self):
        self.cursor.execute("SELECT id, name FROM Otdel")
        self.otdel_map = {name: id for id, name in self.cursor.fetchall()}
        self.cb_otd["values"] = list(self.otdel_map.keys())

        self.cursor.execute("SELECT id, name FROM Postavshik")
        self.post_map = {name: id for id, name in self.cursor.fetchall()}
        self.cb_post["values"] = list(self.post_map.keys())

    def on_filter_change(self, event=None):
        where_clauses = []
        if self.cb_otd.get():
            otdel_id = self.otdel_map[self.cb_otd.get()]
            where_clauses.append(f"t.otdel_id = {otdel_id}")
        if self.cb_post.get():
            post_id = self.post_map[self.cb_post.get()]
            where_clauses.append(f"t.postavshik_id = {post_id}")

        where_sql = " AND ".join(where_clauses)
        if where_sql:
            where_sql = "WHERE " + where_sql

        query = f"""
            SELECT t.name, t.price, t.kolichestvo, t.price * t.kolichestvo AS total
            FROM Tovar t
            {where_sql}
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

        self.calc_sum(where_sql)

    def calc_sum(self, where_sql=""):
        self.cursor.execute(f"SELECT SUM(kolichestvo) FROM Tovar t {where_sql}")
        total = self.cursor.fetchone()[0] or 0.0
        self.sum_label.configure(text=f"Сума кількості: {total:.2f}")

    def reset_filter(self, event=None):
        self.cb_otd.set("")
        self.cb_post.set("")
        self.on_filter_change()

if __name__ == "__main__":
    app = TovarApp()
    app.mainloop()
