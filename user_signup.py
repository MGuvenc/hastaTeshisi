import re
import sqlite3
import sys
from PyQt5.QtGui import QIcon, QRegularExpressionValidator
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout,
                             QFormLayout, QComboBox, QMessageBox)


class HastaKayitEkrani(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        label_ad = QLabel('Ad:')
        label_soyad = QLabel('Soyad:')
        label_yas = QLabel('Yaş:')
        label_cinsiyet = QLabel('Cinsiyet:')
        label_email = QLabel('E-Posta:')
        label_sifre = QLabel('Şifre:')

        self.line_edit_ad = QLineEdit(self)
        self.line_edit_soyad = QLineEdit(self)
        self.line_edit_yas = QLineEdit(self)
        self.line_edit_email = QLineEdit(self)
        self.line_edit_sifre = QLineEdit(self)
        self.line_edit_sifre.setEchoMode(QLineEdit.Password)

        self.combo_cinsiyet = QComboBox(self)
        self.combo_cinsiyet.addItem("Erkek")
        self.combo_cinsiyet.addItem("Kadın")

        btn_kaydet = QPushButton('Kaydol', self)
        btn_kaydet.clicked.connect(self.kaydet_clicked)

        self.setStyleSheet("background-color: #f5f5f5; color: #333;")
        btn_kaydet.setStyleSheet("background-color: #3498db; color: white;"
                                 " border-radius: 5px; padding: 5px;")

        form_layout = QFormLayout()
        form_layout.addRow(label_ad, self.line_edit_ad)
        form_layout.addRow(label_soyad, self.line_edit_soyad)
        form_layout.addRow(label_yas, self.line_edit_yas)
        form_layout.addRow(label_cinsiyet, self.combo_cinsiyet)
        form_layout.addRow(label_email, self.line_edit_email)
        form_layout.addRow(label_sifre, self.line_edit_sifre)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(btn_kaydet)

        self.setLayout(main_layout)

        width = 400
        height = 300
        self.setFixedSize(width, height)

        icon = QIcon('firat_uni.png')
        self.setWindowIcon(icon)

        self.setWindowTitle('Hasta Kayıt Ekranı')
        self.show()

    def kaydet_clicked(self):
        if self._kontrol_veriler:
            reply = QMessageBox.question(self, 'Onay', 'Verilerinizin kaydedilmesini onaylıyor musunuz?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._kaydet_veriler()
            else:
                QMessageBox.information(self, 'İptal', 'Kaydetme işlemi iptal edildi.')
        else:
            QMessageBox.warning(self, 'Uyarı', 'Eksik veya geçersiz bilgiler. Lütfen kontrol edin.')

    def _kontrol_veriler(self):
        email = self.line_edit_email.text()
        sifre = self.line_edit_sifre.text()

        if not email or not sifre:
            return False

        return True

    def _kaydet_veriler(self):
        try:
            veriler = {
                'ad': self.line_edit_ad.text,
                'soyad': self.line_edit_soyad.text,
                'yas': self.line_edit_yas.text,
                'cinsiyet': self.combo_cinsiyet.currentText,
                'teshis': 0
            }

            with sqlite3.connect('hasta_teshis.db') as db:
                db.execute(
                    "INSERT INTO Hasta (ad, soyad, yas, cinsiyet, teshis) "
                    "VALUES (:ad, :soyad, :yas, :cinsiyet, :teshis)",
                    veriler)
                db.commit()
                db.close()
            QMessageBox.information(self, 'Onay', 'Kaydetme işlemi başarılı.')

        except Exception as e:
            QMessageBox.warning(self, 'Hata', str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    hasta_kayit_ekrani = HastaKayitEkrani()

    hasta_kayit_ekrani.show()
    sys.exit(app.exec_())
