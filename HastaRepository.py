import sqlite3


class HastaRepository:
    def __init__(self, db_path='hasta_teshis.db'):
        self.db_path = db_path

    def kaydet(self, hasta):
        try:
            db = sqlite3.connect(self.db_path)
            cursor = db.cursor()

            cursor.execute(
                "INSERT INTO Hasta (ad, soyad, dogum_tarihi, cinsiyet, mail, sifre) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (hasta.ad, hasta.soyad, hasta.dogum_tarihi, hasta.cinsiyet, hasta.mail, hasta.sifre))

            db.commit()
            db.close()

            return True
        except Exception as e:
            print(str(e))
            return False
