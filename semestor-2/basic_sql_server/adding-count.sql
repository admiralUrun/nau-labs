ALTER TABLE Tovar
ADD COLUMN kolichestvo INT DEFAULT 1;


UPDATE Tovar SET kolichestvo = 10 WHERE name = 'iPhone 14';
UPDATE Tovar SET kolichestvo = 5 WHERE name = 'Galaxy S22';
UPDATE Tovar SET kolichestvo = 20 WHERE name = 'Апельсин';
