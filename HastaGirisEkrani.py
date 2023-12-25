import sys
import hashlib
import re

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFormLayout, QVBoxLayout, QMessageBox, QCheckBox
)
from HastaRepository import HastaRepository
from HastaKayitEkrani import HastaKayitEkrani


class HastaGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()

        self.kayit_ekrani = HastaKayitEkrani(self)
        self.line_edit_email = QLineEdit(self)
        self.line_edit_sifre = QLineEdit(self)
        self.check_box_hatirla = QCheckBox("Beni Hatırla", self)

        self.init_ui()

    def init_ui(self):
        label_email = QLabel('E-Posta:')
        label_sifre = QLabel('Şifre:')

        self.line_edit_sifre.setEchoMode(QLineEdit.Password)

        btn_giris = QPushButton('Giriş Yap', self)
        btn_giris.clicked.connect(self.giris_clicked)

        btn_kayit_ekrani = QPushButton('Kayıt Ekranı', self)
        btn_kayit_ekrani.clicked.connect(self.show_kayit_ekrani)

        self.setStyleSheet("background-color: #f5f5f5; color: #333;")
        btn_giris.setStyleSheet("background-color: #3498db; color: white;"
                                " border-radius: 5px; padding: 5px;")

        form_layout = QFormLayout()
        form_layout.addRow(label_email, self.line_edit_email)
        form_layout.addRow(label_sifre, self.line_edit_sifre)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.check_box_hatirla)
        button_layout.addWidget(btn_giris)
        button_layout.addWidget(btn_kayit_ekrani)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        width = 400
        height = 300
        self.setFixedSize(width, height)

        self.setWindowTitle('Hasta Giriş Ekranı')
        self.setWindowIcon(QIcon('firat_uni.png'))

    def giris_clicked(self):
        mail = self.line_edit_email.text()
        sifre = self.md5_hash(self.line_edit_sifre.text())

        hatirla_durumu = self.check_box_hatirla.isChecked()
        mail_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$')

        if not mail_pattern.match(mail):
            QMessageBox.warning(self, 'Uyarı', 'Geçerli bir e-posta adresi girin.')
            return

        hasta_repository = HastaRepository()
        hasta = hasta_repository.getir_by_mail(mail)

        if hasta is not None and hasta.sifre == sifre:
            QMessageBox.information(self, 'Başarılı', 'Giriş başarılı.')
        else:
            QMessageBox.warning(self, 'Hata', 'E-posta veya şifre yanlış.')

    def show_kayit_ekrani(self):
        self.kayit_ekrani.show()
        self.hide()

    @staticmethod
    def md5_hash(password):
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        return hashed_password


def main():
    app = QApplication(sys.argv)
    hasta_giris_ekrani = HastaGirisEkrani()
    hasta_giris_ekrani.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
