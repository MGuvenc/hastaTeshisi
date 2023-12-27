import sqlite3
from Hasta import Hasta


class HastaRepository:
    def __init__(self, db_path='hasta_teshis.db'):
        self.db_path = db_path

    def mail_var_mi(self, mail):
        try:
            db = sqlite3.connect(self.db_path)
            cursor = db.cursor()

            cursor.execute("SELECT COUNT(*) FROM Hasta WHERE mail = ?", (mail,))
            count = cursor.fetchone()[0]

            db.close()

            return count > 0
        except Exception as e:
            print(str(e))
            return False

    def getir_by_mail(self, mail):
        try:
            db = sqlite3.connect(self.db_path)
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Hasta WHERE mail=?", (mail,))
            data = cursor.fetchone()
            db.close()
            if data:
                return Hasta(*data)
            else:
                return None
        except:
            return None

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
