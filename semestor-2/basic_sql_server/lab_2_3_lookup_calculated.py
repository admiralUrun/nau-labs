import customtkinter as ctk
import mysql.connector
from tkinter import ttk

class LookupApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Товари з LookUp та Сумою")
        self.geometry("900x500")
        self.minsize(600, 400)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="📦 Таблиця товарів (з LookUp та Сумою)", font=("Arial", 18, "bold"))
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.table = ttk.Treeview(self.container, show="headings", style="Treeview")
        self.table.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.status = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status.grid(row=2, column=0, sticky="w", padx=10)

        self.load_data()

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1",
                database="market"
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    T.name AS Товар,
                    O.name AS Відділ,
                    V.name AS Вид,
                    P.name AS Постачальник,
                    T.kolichestvo AS Кількість,
                    T.price AS Ціна,
                    (T.kolichestvo * T.price) AS Сума
                FROM Tovar T
                JOIN Otdel O ON T.otdel_id = O.id
                JOIN Vid V ON T.vid_id = V.id
                JOIN Postavshik P ON T.postavshik_id = P.id
            """)

            columns = [desc[0] for desc in cursor.description]
            self.table["columns"] = columns
            for col in columns:
                self.table.heading(col, text=col)
                self.table.column(col, anchor="center", width=120, stretch=True)

            for row in cursor.fetchall():
                self.table.insert("", "end", values=row)

            self.status.configure(text=f"✅ Завантажено {len(self.table.get_children())} записів.")
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            self.status.configure(text=f"❌ Помилка підключення: {err}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = LookupApp()
    app.mainloop()