import hashlib
import re
import sys

from PyQt5.QtCore import QDate, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QFormLayout, QComboBox, QMessageBox, QDateEdit, QApplication
)

from Hasta import Hasta
from HastaRepository import HastaRepository


class HastaKayitEkrani(QWidget):
    def __init__(self):
        super().__init__()

        self.combo_cinsiyet = QComboBox(self)
        self.line_edit_sifre = QLineEdit(self)
        self.line_edit_email = QLineEdit(self)
        self.line_edit_ad = QLineEdit(self)
        self.line_edit_soyad = QLineEdit(self)
        self.date_edit_dogum_tarihi = QDateEdit(self)
        self.init_ui()

    def init_ui(self):
        label_ad = QLabel('Ad:')
        label_soyad = QLabel('Soyad:')
        label_dogum_tarihi = QLabel('Doğum Tarihi:')
        label_cinsiyet = QLabel('Cinsiyet:')
        label_email = QLabel('E-Posta:')
        label_sifre = QLabel('Şifre:')

        self.date_edit_dogum_tarihi.setCalendarPopup(True)
        self.date_edit_dogum_tarihi.setDate(QDate.currentDate())
        self.date_edit_dogum_tarihi.setMaximumDate(QDate.currentDate().addYears(-18))
        self.line_edit_sifre.setEchoMode(QLineEdit.Password)

        self.combo_cinsiyet.addItem("Erkek")
        self.combo_cinsiyet.addItem("Kadın")

        btn_kaydet = QPushButton('Kaydol', self)
        btn_kaydet.clicked.connect(self.kaydet_clicked)

        self.setStyleSheet("background-color: #f5f5f5; color: #333;")
        btn_kaydet.setStyleSheet("background-color: #3498db; color: white;"
                                 " border-radius: 5px; padding: 5px;")

        form_layout = QFormLayout()

        # Ad ve soyad için sadece harf girişi kabul eden validator'ları ayarla
        ad_validator = QRegExpValidator(QRegExp("^[a-zA-Z]*$"))
        self.line_edit_ad.setValidator(ad_validator)

        soyad_validator = QRegExpValidator(QRegExp("^[a-zA-Z]*$"))
        self.line_edit_soyad.setValidator(soyad_validator)

        form_layout.addRow(label_ad, self.line_edit_ad)
        form_layout.addRow(label_soyad, self.line_edit_soyad)
        form_layout.addRow(label_dogum_tarihi, self.date_edit_dogum_tarihi)
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

    @staticmethod
    def md5_hash(password):
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        return hashed_password

    def _kontrol_veriler(self):
        ad = self.line_edit_ad.text()
        soyad = self.line_edit_soyad.text()
        dogum_tarihi = self.date_edit_dogum_tarihi.date().toString("yyyy-MM-dd")
        cinsiyet = self.combo_cinsiyet.currentText()
        mail = self.line_edit_email.text()
        sifre = self.md5_hash(self.line_edit_sifre.text())
        mail_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$')

        if not all([ad, soyad, dogum_tarihi, cinsiyet, mail, sifre]):
            QMessageBox.warning(self, 'Uyarı', 'Tüm alanları doldurun.')
            return None
        elif not mail_pattern.match(mail):
            QMessageBox.warning(self, 'Uyarı', 'Geçerli bir e-posta adresi girin.')
            return None

        veriler = {
            'ad': ad,
            'soyad': soyad,
            'dogum_tarihi': dogum_tarihi,
            'cinsiyet': cinsiyet,
            'mail': mail,
            'sifre': sifre
        }

        return veriler

    def kaydet_clicked(self):
        veriler = self._kontrol_veriler()
        if veriler is not None:
            hasta = Hasta(**veriler)
            hasta_repository = HastaRepository()
            if hasta_repository.kaydet(hasta):
                QMessageBox.information(self, 'Onay', 'Kaydetme işlemi başarılı.')
            else:
                QMessageBox.warning(self, 'Hata', 'Kaydetme işlemi sırasında bir hata oluştu.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    hasta_kayit_ekrani = HastaKayitEkrani()

    hasta_kayit_ekrani.show()
    sys.exit(app.exec_())
