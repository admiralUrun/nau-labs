import customtkinter as ctk
import mysql.connector
from tkinter import ttk

class SQLViewer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Market Table Viewer")
        self.geometry("800x500")
        self.minsize(500, 300)

        style = ttk.Style(self)
        style.theme_use("clam")  # або "default"

        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#000000",
                        rowheight=30,
                        fieldbackground="#ffffff",
                        borderwidth=1,
                        relief="solid"
                        )

        style.configure("Treeview.Heading",
                        background="#f0f0f0",
                        foreground="black",
                        borderwidth=1,
                        relief="solid"
                        )

        # Сітка
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Заголовок
        self.title_label = ctk.CTkLabel(self, text="📊 Таблиця товарів (База: market)", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, sticky="we", padx=10, pady=(10, 5))

        # Контейнер таблиці
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.table = ttk.Treeview(self.container)
        self.table.grid(row=0, column=0, sticky="nsew")

        # Скролбар
        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Статус
        self.status_label = ctk.CTkLabel(self, text="🔄 Завантаження...", font=("Arial", 14))
        self.status_label.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 10))

        # Кнопка оновлення
        self.refresh_button = ctk.CTkButton(self, text="🔁 Оновити", command=self.load_data, width=120)
        self.refresh_button.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=15)

        self.load_data()

    def load_data(self):
        # Очистити попередні дані
        for row in self.table.get_children():
            self.table.delete(row)

        try:
            self.status_label.configure(text="🔄 Завантаження з бази...")
            conn = mysql.connector.connect(
                host="localhost",
                port=3306,
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
                    T.price AS Ціна
                FROM Tovar T
                JOIN Otdel O ON T.otdel_id = O.id
                JOIN Vid V ON T.vid_id = V.id
                JOIN Postavshik P ON T.postavshik_id = P.id
            """)

            columns = [desc[0] for desc in cursor.description]
            self.table["columns"] = columns
            self.table["show"] = "headings"

            # При створенні Treeview
            # self.table = ttk.Treeview(self.container, show="headings", style="Treeview")

            # У load_data (для кожного стовпця)
            for col in columns:
                self.table.heading(col, text=col)
                self.table.column(col, anchor="center", stretch=True, width=100)

            rows = cursor.fetchall()
            for row in rows:
                self.table.insert("", "end", values=row)

            if not rows:
                self.status_label.configure(text="⚠️ Даних немає (таблиця порожня)")
            else:
                self.status_label.configure(text=f"✅ Успішно завантажено {len(rows)} рядків")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            self.status_label.configure(text=f"❌ Помилка: {err}")
            self.table["columns"] = ["Error"]
            self.table["show"] = "headings"
            self.table.heading("Error", text="Помилка")
            self.table.insert("", "end", values=[str(err)])

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = SQLViewer()
    app.mainloop()
