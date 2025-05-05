
CREATE TABLE Otdel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Vid (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Postavshik (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Tovar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    otdel_id INT,
    vid_id INT,
    postavshik_id INT,
    price DECIMAL(10,2),
    FOREIGN KEY (otdel_id) REFERENCES Otdel(id),
    FOREIGN KEY (vid_id) REFERENCES Vid(id),
    FOREIGN KEY (postavshik_id) REFERENCES Postavshik(id)
);