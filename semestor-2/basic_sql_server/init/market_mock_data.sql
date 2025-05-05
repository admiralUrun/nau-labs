-- Додати записи у таблицю Otdel
INSERT INTO Otdel (name) VALUES 
('Електроніка'),
('Продукти'),
('Одяг');

-- Додати записи у таблицю Vid
INSERT INTO Vid (name) VALUES 
('Смартфони'),
('Ноутбуки'),
('Фрукти'),
('Куртки');

-- Додати записи у таблицю Postavshik
INSERT INTO Postavshik (name) VALUES 
('Samsung'),
('Apple'),
('FreshFarm'),
('Zara');

-- Додати записи у таблицю Tovar
INSERT INTO Tovar (name, otdel_id, vid_id, postavshik_id, price) VALUES
('iPhone 14', 1, 1, 2, 999.99),
('Galaxy S22', 1, 1, 1, 899.99),
('MacBook Pro', 1, 2, 2, 1999.99),
('Апельсин', 2, 3, 3, 2.50),
('Зимова куртка', 3, 4, 4, 149.99),
('Банан', 2, 3, 3, 1.99),
('Куртка демісезонна', 3, 4, 4, 129.99),
('Xiaomi Redmi Note', 1, 1, 1, 499.90);