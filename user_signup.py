import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QComboBox


class HastaKayitEkrani(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        label_ad = QLabel('Ad:')
        label_soyad = QLabel('Soyad:')
        label_yas = QLabel('Yaş:')
        label_cinsiyet = QLabel('Cinsiyet:')

        line_edit_ad = QLineEdit(self)
        line_edit_soyad = QLineEdit(self)
        line_edit_yas = QLineEdit(self)

        combo_cinsiyet = QComboBox(self)
        combo_cinsiyet.addItem("Erkek")
        combo_cinsiyet.addItem("Kadın")

        btn_kaydet = QPushButton('Kaydet', self)
        btn_kaydet.clicked.connect(self.kaydet_clicked)

        self.setStyleSheet("background-color: #f5f5f5; color: #333;")  # Arka plan rengi ve metin rengi
        btn_kaydet.setStyleSheet("background-color: #3498db; color: white; border-radius: 5px; padding: 5px;")

        form_layout = QFormLayout()
        form_layout.addRow(label_ad, line_edit_ad)
        form_layout.addRow(label_soyad, line_edit_soyad)
        form_layout.addRow(label_yas, line_edit_yas)
        form_layout.addRow(label_cinsiyet, combo_cinsiyet)

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
        # to-do
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    hasta_kayit_ekrani = HastaKayitEkrani()
    sys.exit(app.exec_())
