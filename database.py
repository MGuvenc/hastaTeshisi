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
            dogum_tarihi TEXT NOT NULL,
            cinsiyet TEXT NOT NULL,
            mail TEXT NOT NULL,
            sifre TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MRGoruntuleri (
            id INTEGER PRIMARY KEY,
            hasta_id INTEGER,
            model TEXT NOT NULL,
            goruntu_path TEXT NOT NULL,
            FOREIGN KEY (hasta_id) REFERENCES Hasta(id)
        )
    ''')

    conn.commit()


def insert_into_mrgoruntuleri(conn, hasta_id, model, goruntu_path):
    cur = conn.cursor()
    try:
        query = '''INSERT INTO MRGoruntuleri (hasta_id, model, goruntu_path) 
                   VALUES (?, ?, ?)'''
        cur.execute(query, (hasta_id, model, goruntu_path))
        conn.commit()
        print("Resim ve model başarıyla eklendi.")
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
    finally:
        cur.close()


def close_connection(conn):
    conn.close()
