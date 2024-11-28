import sqlite3
from prettytable import PrettyTable

# Підключення до бази даних
connection = sqlite3.connect('pharmacy.db')
cursor = connection.cursor()

# Очищення таблиць, якщо вони існують
cursor.execute("DROP TABLE IF EXISTS medicines;")
cursor.execute("DROP TABLE IF EXISTS suppliers;")
cursor.execute("DROP TABLE IF EXISTS deliveries;")

# Створення таблиці "Ліки"
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines (
    registration_number INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    manufacture_date DATE NOT NULL,
    shelf_life_days INTEGER CHECK (shelf_life_days > 0),
    category VARCHAR(50) CHECK (category IN ('Протизапальне', 'Знеболююче', 'Вітаміни')),
    price NUMERIC(10, 2) CHECK (price > 0),
    prescription_required BOOLEAN NOT NULL
);
""")

# Створення таблиці "Постачальники"
cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone CHAR(10) NOT NULL,
    contact_person VARCHAR(255),
    location VARCHAR(50) CHECK (location IN ('Україна', 'Інша країна'))
);
""")

# Створення таблиці "Поставки"
cursor.execute("""
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id INTEGER PRIMARY KEY,
    delivery_date DATE NOT NULL,
    medicine_id INTEGER REFERENCES medicines(registration_number) ON DELETE CASCADE,
    quantity INTEGER CHECK (quantity > 0),
    supplier_id INTEGER REFERENCES suppliers(supplier_id) ON DELETE CASCADE
);
""")

# Наповнення таблиці "Ліки" даними
cursor.executemany("""
INSERT INTO medicines (registration_number, name, manufacture_date, shelf_life_days, category, price, prescription_required)
VALUES (?, ?, ?, ?, ?, ?, ?);
""", [
    (1, 'Ібупрофен', '2024-01-01', 730, 'Протизапальне', 100.00, 1),
    (2, 'Парацетамол', '2023-12-01', 365, 'Знеболююче', 50.00, 0),
    (3, 'Вітамін С', '2024-03-01', 180, 'Вітаміни', 30.00, 0),
    (4, 'Диклофенак', '2023-11-15', 365, 'Протизапальне', 120.00, 1),
    (5, 'Аспірин', '2024-02-01', 365, 'Знеболююче', 80.00, 0),
    (6, 'Магній В6', '2024-01-10', 730, 'Вітаміни', 150.00, 0),
    (7, 'Нурофен', '2023-12-25', 365, 'Знеболююче', 90.00, 1),
    (8, 'Кальцій Д3', '2024-03-15', 180, 'Вітаміни', 110.00, 0),
    (9, 'Флуконазол', '2023-11-20', 730, 'Протизапальне', 140.00, 1),
    (10, 'Терафлю', '2024-02-05', 365, 'Знеболююче', 70.00, 0),
    (11, 'Омега-3', '2023-10-15', 730, 'Вітаміни', 200.00, 0),
    (12, 'Анальгін', '2024-01-20', 365, 'Знеболююче', 60.00, 1),
    (13, 'Цитрамон', '2023-12-30', 365, 'Знеболююче', 40.00, 0)
])

# Наповнення таблиці "Постачальники" даними
cursor.executemany("""
INSERT INTO suppliers (supplier_id, name, address, phone, contact_person, location)
VALUES (?, ?, ?, ?, ?, ?);
""", [
    (1, 'Аптека-Люкс', 'Київ, вул. Хрещатик, 1', '0931234567', 'Іван Іванов', 'Україна'),
    (2, 'МедФарм', 'Львів, вул. Шевченка, 10', '0937654321', 'Петро Петров', 'Україна'),
    (3, 'Фарма-Експорт', 'Варшава, Польща', '0931112223', 'Олена Олененко', 'Інша країна'),
    (4, 'Здоров\'я Плюс', 'Одеса, вул. Дерибасівська, 5', '0932223334', 'Анна Ананенко', 'Україна'),
    (5, 'Медика', 'Берлін, Німеччина', '0934445556', 'Карл Шмідт', 'Інша країна')
])

# Наповнення таблиці "Поставки" даними
cursor.executemany("""
INSERT INTO deliveries (delivery_id, delivery_date, medicine_id, quantity, supplier_id)
VALUES (?, ?, ?, ?, ?);
""", [
    (1, '2024-01-05', 1, 50, 1),
    (2, '2024-01-10', 2, 100, 2),
    (3, '2024-01-15', 3, 200, 3),
    (4, '2024-01-20', 4, 30, 1),
    (5, '2024-01-25', 1, 60, 3),
    (6, '2024-01-30', 2, 70, 2),
    (7, '2024-02-01', 5, 40, 4),
    (8, '2024-02-05', 6, 80, 5),
    (9, '2024-02-10', 7, 25, 1),
    (10, '2024-02-15', 8, 35, 2),
    (11, '2024-02-20', 9, 45, 3)
])

# Збереження змін
connection.commit()

# Функція для виконання запитів і друку таблиць
def execute_and_print_query(query, headers):
    cursor.execute(query)
    rows = cursor.fetchall()
    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row(row)
    print(table)

# 1. Ліки, які відпускаються за рецептом
print("\n1. Ліки, які відпускаються за рецептом:")
query = """
    SELECT name AS 'Назва ліків'
    FROM medicines
    WHERE prescription_required = 1
    ORDER BY name;
"""
execute_and_print_query(query, ["Назва ліків"])

# 2. Ліки за обраною групою
selected_group = input("\nВведіть групу ліків (Протизапальне, Знеболююче, Вітаміни): ")
query = f"""
    SELECT name AS 'Назва ліків'
    FROM medicines
    WHERE category = '{selected_group}';
"""
print(f"\nЛіки у групі '{selected_group}':")
execute_and_print_query(query, ["Назва ліків"])

# 3. Вартість кожної поставки
print("\n3. Вартість кожної поставки:")
query = """
    SELECT d.delivery_id AS 'ID поставки',
           m.name AS 'Назва ліків',
           (m.price * d.quantity) AS 'Загальна вартість'
    FROM deliveries d
    JOIN medicines m ON d.medicine_id = m.registration_number;
"""
execute_and_print_query(query, ["ID поставки", "Назва ліків", "Загальна вартість"])

# 4. Загальна сума грошей для кожного постачальника
print("\n4. Загальна сума грошей для кожного постачальника:")
query = """
    SELECT s.name AS 'Назва постачальника',
           SUM(m.price * d.quantity) AS 'Загальна сума'
    FROM deliveries d
    JOIN medicines m ON d.medicine_id = m.registration_number
    JOIN suppliers s ON d.supplier_id = s.supplier_id
    GROUP BY s.name;
"""
execute_and_print_query(query, ["Назва постачальника", "Загальна сума"])

# 5. Кількість поставок для кожної групи ліків
print("\n5. Кількість поставок для кожної групи ліків:")
query = """
    SELECT m.category AS 'Група ліків',
           s.location AS 'Локація постачальника',
           COUNT(d.delivery_id) AS 'Кількість поставок'
    FROM deliveries d
    JOIN medicines m ON d.medicine_id = m.registration_number
    JOIN suppliers s ON d.supplier_id = s.supplier_id
    GROUP BY m.category, s.location;
"""
execute_and_print_query(query, ["Група ліків", "Локація постачальника", "Кількість поставок"])

# 6. Остання дата придатності для кожної ліки
print("\n6. Остання дата придатності для кожної ліки:")
query = """
    SELECT name AS 'Назва ліків',
           MAX(DATE(manufacture_date, '+' || shelf_life_days || ' days')) AS 'Дата придатності'
    FROM medicines
    GROUP BY name;
"""
execute_and_print_query(query, ["Назва ліків", "Дата придатності"])

# Закриття з'єднання
cursor.close()
connection.close()