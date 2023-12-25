import sys
import hashlib
import re
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QFormLayout, QComboBox, QMessageBox, QDateEdit, QApplication, QDialog
)

from Hasta import Hasta
from HastaRepository import HastaRepository


class DogrulamaEkrani(QDialog):
    def __init__(self, parent, dogrulama_kodu):
        super().__init__(parent)

        self.parent = parent
        self.dogrulama_kodu = dogrulama_kodu
        self.line_edit_dogrulama_kodu = QLineEdit(self)
        self.init_ui()

    def init_ui(self):
        label_dogrulama_kodu = QLabel('Doğrulama Kodu:')
        btn_dogrula = QPushButton('Doğrula', self)
        btn_dogrula.clicked.connect(self.dogrula_clicked)

        form_layout = QFormLayout()
        form_layout.addRow(label_dogrulama_kodu, self.line_edit_dogrulama_kodu)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(btn_dogrula)

        self.setLayout(main_layout)

        self.setWindowTitle('Doğrulama Ekranı')

        regex = QRegExp("^\d{6}$")
        validator = QRegExpValidator(regex)
        self.line_edit_dogrulama_kodu.setValidator(validator)

    def dogrula_clicked(self):
        dogrulama_kodu = self.line_edit_dogrulama_kodu.text()
        if dogrulama_kodu == str(self.dogrulama_kodu):
            self.accept()
        else:
            QMessageBox.warning(self, 'Uyarı', 'Doğrulama kodu geçersiz.')


class HastaKayitEkrani(QWidget):
    def __init__(self, hasta_giris_ekrani):
        super().__init__()

        self.dogrulama_ekrani = None
        self.hasta_giris_ekrani = hasta_giris_ekrani

        self.combo_cinsiyet = QComboBox(self)
        self.line_edit_sifre = QLineEdit(self)
        self.line_edit_email = QLineEdit(self)
        self.line_edit_ad = QLineEdit(self)
        self.line_edit_soyad = QLineEdit(self)
        self.date_edit_dogum_tarihi = QDateEdit(self)
        self.dogrulama_kodu = None

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
        btn_kaydet.clicked.connect(self.on_kaydet_clicked)

        btn_giris_ekrani = QPushButton('Giriş Ekranı', self)
        btn_giris_ekrani.clicked.connect(self.show_giris_ekrani)

        self.setStyleSheet("background-color: #f5f5f5; color: #333;")
        btn_kaydet.setStyleSheet("background-color: #3498db; color: white;"
                                 " border-radius: 5px; padding: 5px;")

        form_layout = QFormLayout()
        ad_validator = QRegExpValidator(QRegExp("^[a-zA-ZğüşıöçĞÜŞİÖÇ]*$"))
        soyad_validator = QRegExpValidator(QRegExp("^[a-zA-ZğüşıöçĞÜŞİÖÇ]*$"))

        self.line_edit_ad.setValidator(ad_validator)
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
        main_layout.addWidget(btn_giris_ekrani)

        self.setLayout(main_layout)

        width = 400
        height = 300
        self.setFixedSize(width, height)

        self.setWindowTitle('Hasta Kayıt Ekranı')
        self.setWindowIcon(QIcon('firat_uni.png'))

    @staticmethod
    def md5_hash(password):
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        return hashed_password

    def _kontrol_veriler(self):
        ad = self.line_edit_ad.text().capitalize()
        soyad = self.line_edit_soyad.text().upper()
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
        elif len(self.line_edit_sifre.text()) < 6:
            QMessageBox.warning(self, 'Uyarı', 'Şifre en az 6 karakter olmalıdır.')
            return None

        self.veriler = {
            'ad': ad,
            'soyad': soyad,
            'dogum_tarihi': dogum_tarihi,
            'cinsiyet': cinsiyet,
            'mail': mail,
            'sifre': sifre
        }

        return self.veriler

    def on_kaydet_clicked(self):
        veriler = self._kontrol_veriler()
        if veriler is not None:
            mail = veriler['mail']
            hasta_repository = HastaRepository()

            if hasta_repository.mail_var_mi(mail):
                QMessageBox.warning(self, 'Uyarı', 'Bu e-posta adresi zaten kayıtlı.')
            else:
                onay = self.onay_al("Kaydetme İşlemi", "Verilerinizi kaydedilmesini onaylıyor musunuz?")
                if onay == QMessageBox.Yes:
                    self.dogrulama_kodu_al()
                else:
                    QMessageBox.warning(self, 'İptal', 'Kaydetme işlemi iptal edildi.')

    def onay_al(self, baslik, mesaj):
        onay = QMessageBox.question(self, baslik, mesaj, QMessageBox.Yes | QMessageBox.No)
        return onay

    def show_giris_ekrani(self):
        self.hasta_giris_ekrani.show()
        self.hide()

    def dogrulama_kodu_al(self):
        try:
            sender_email = "hastateshis@gmail.com"
            receiver_email = self.line_edit_email.text()
            app_password = "xbvb isym jqwy vzdz"

            subject = "Doğrulama Kodu"
            self.dogrulama_kodu = random.randint(100000, 999999)
            body = (f"Merhaba {self.line_edit_ad.text().capitalize()} {self.line_edit_soyad.text().upper()}! "
                    f"Aramıza hoş geldiniz. Doğrulama kodunuz: {self.dogrulama_kodu}")

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receiver_email, message.as_string())

            QMessageBox.information(self, 'Doğrulama Kodu', f"Doğrulama kodu {receiver_email} adresine gönderildi.")

            self.dogrulama_ekrani = DogrulamaEkrani(self, self.dogrulama_kodu)
            if self.dogrulama_ekrani.exec_() == QDialog.Accepted:
                hasta = Hasta(**self.veriler)
                hasta_repository = HastaRepository()
                if hasta_repository.kaydet(hasta):
                    QMessageBox.information(self, 'Onay', 'Kaydetme işlemi başarılı.')
                else:
                    QMessageBox.warning(self, 'Hata', 'Kaydetme işlemi sırasında bir hata oluştu.')
            else:
                QMessageBox.warning(self, 'Uyarı', 'Doğrulama kodu girmeden kayıt yapılamaz.')

        except smtplib.SMTPConnectError as e:
            QMessageBox.warning(self, 'Hata', f"SMTP bağlantı hatası: {str(e)}")
        except smtplib.SMTPAuthenticationError as e:
            QMessageBox.warning(self, 'Hata', f"SMTP kimlik doğrulama hatası: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f"Doğrulama kodu gönderilirken bir hata oluştu: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    hasta_kayit_ekrani = HastaKayitEkrani(None)
    hasta_kayit_ekrani.show()
    sys.exit(app.exec_())