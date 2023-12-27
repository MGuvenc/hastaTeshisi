from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QFormLayout, QComboBox, QLineEdit, QFileDialog, QSizePolicy, QMenuBar
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class AnaSayfa(QMainWindow):
    def __init__(self, hasta_adi, hasta_soyadi):
        super().__init__()

        self.hasta_adi = hasta_adi
        self.hasta_soyadi = hasta_soyadi
        self.setFixedSize(400, 300)
        self.setWindowTitle('Veri Giriş Ekranı')
        self.setWindowIcon(QIcon('firat_uni.png'))

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        option_box = QHBoxLayout()

        option_combobox = QComboBox()
        option_combobox.addItems(['Alzheimer', 'Breast Cancer', 'Brain Tumor'])

        option_box.addWidget(option_combobox)

        image_upload_button = QPushButton('Resim Yükle')
        send_button = QPushButton('Analiz Et')

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_upload_button.clicked.connect(self.load_image)

        send_button.clicked.connect(self.send_data)
        send_button.setStyleSheet("background-color: #3498db; color: white;"
                                  "border-radius: 5px; padding: 5px;")

        option_layout = QFormLayout()
        option_layout.addRow('Model:', option_combobox)
        option_layout.addRow('Veri:', image_upload_button)
        option_layout.addRow('', image_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(option_layout)
        main_layout.addWidget(send_button)

        central_widget.setLayout(main_layout)

        menubar = QMenuBar()
        self.setMenuBar(menubar)
        profil = menubar.addMenu(f'{self.hasta_adi} {self.hasta_soyadi}')
        profil.addAction('Çıkış', self.close)

    def load_image(self):
        pass
        # To-do

    def send_data(self):
        pass
        # To-do


def main():
    app = QApplication(sys.argv)
    ana_sayfa = AnaSayfa('', '')
    ana_sayfa.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
