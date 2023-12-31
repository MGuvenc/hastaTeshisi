import hashlib
import sys
import traceback

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFormLayout, QVBoxLayout, QMessageBox, QCheckBox
)

from AnaSayfa import AnaSayfa
from HastaKayitEkrani import HastaKayitEkrani
from HastaRepository import HastaRepository


class HastaGirisEkrani(QWidget):
    def __init__(self):
        super().__init__()

        self.kayit_ekrani = HastaKayitEkrani(self)
        self.anasayfa = None
        self.line_edit_email = QLineEdit(self)
        self.line_edit_sifre = QLineEdit(self)
        self.check_box_hatirla = QCheckBox("Beni Hatırla", self)

        self.settings = QSettings("FiratUni", "HastaGirisEkrani")

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

        self.check_box_hatirla.setChecked(self.settings.value("BeniHatirla", False, type=bool))
        if self.check_box_hatirla.isChecked():
            self.line_edit_email.setText(self.settings.value("KayitEmail", "", type=str))
            self.line_edit_sifre.setText(self.settings.value("KayitSifre", "", type=str))

    def giris_clicked(self):
        try:
            mail = self.line_edit_email.text()
            sifre = self.line_edit_sifre.text()

            if not mail or not sifre:
                QMessageBox.warning(self, 'Uyarı', 'Lütfen tüm alanları doldurun.')
                return

            hashed_password = self.md5_hash(sifre)

            hasta_repository = HastaRepository()
            hasta = hasta_repository.getir_by_mail(mail)

            if hasta:
                if hasta.sifre == hashed_password:
                    self.anasayfa = AnaSayfa(hasta.id, hasta.ad, hasta.soyad)
                    self.anasayfa.show()
                    self.on_login_successful()
                    if self.check_box_hatirla.isChecked():
                        self.settings.setValue("BeniHatirla", True)
                        self.settings.setValue("KayitEmail", mail)
                        self.settings.setValue("KayitSifre", sifre)
                    else:
                        self.settings.setValue("BeniHatirla", False)
                        self.settings.setValue("KayitEmail", "")
                        self.settings.setValue("KayitSifre", "")
                else:
                    QMessageBox.warning(self, 'Uyarı', 'Kullanıcı adı veya şifre yanlış.')
            else:
                QMessageBox.warning(self, 'Uyarı', 'Kullanıcı adı veya şifre yanlış.')
        except Exception as e:
            print("Exception occurred:", str(e))
            traceback.print_exc()
            QMessageBox.critical(self, '404', f'Beklenmedik bir sorun oluştu: {str(e)}')

    def show_kayit_ekrani(self):
        self.kayit_ekrani = HastaKayitEkrani(self)
        self.kayit_ekrani.show()
        self.on_login_successful()

    def on_login_successful(self):
        self.close()

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
