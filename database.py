import sqlite3


def create_connection(database_path):
    return sqlite3.connect(database_path)


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Hasta (
            id INTEGER PRIMARY KEY,
            ad TEXT NOT NULL,
            soyad TEXT NOT NULL,
            yas INTEGER,
            cinsiyet TEXT,
            teshis TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MRGoruntuleri (
            id INTEGER PRIMARY KEY,
            hasta_id INTEGER,
            goruntu_path TEXT NOT NULL,
            FOREIGN KEY (hasta_id) REFERENCES Hasta(id)
        )
    ''')

    conn.commit()


def close_connection(conn):
    conn.close()
