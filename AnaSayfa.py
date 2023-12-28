import sys
import uuid
import os
import cv2
import sqlite3
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QFormLayout, QComboBox, QFileDialog, QMenuBar, QMainWindow
from PyQt5.QtWidgets import QMessageBox

from database import insert_into_mrgoruntuleri


class AnaSayfa(QMainWindow):
    def __init__(self, hasta_id=1, hasta_adi='', hasta_soyadi=''):
        super().__init__()

        self.unique_filename = None
        self.selected_option = None
        self.image_path = None
        self.filename_label = None
        self.hasta_id = hasta_id
        self.hasta_adi = hasta_adi
        self.hasta_soyadi = hasta_soyadi
        self.setFixedSize(400, 300)
        self.setWindowTitle('Veri Giriş Ekranı')
        self.setWindowIcon(QIcon('firat_uni.png'))
        self.image_label = QLabel()
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

        self.filename_label = QLabel()
        self.image_label = QLabel()
        self.selected_option = option_combobox.currentText()
        image_upload_button.clicked.connect(self.load_image)

        send_button.clicked.connect(self.send_data)
        send_button.setStyleSheet("background-color: #3498db; color: white;"
                                  "border-radius: 5px; padding: 5px;")

        option_layout = QFormLayout()
        option_layout.addRow('Model Seç:', option_combobox)
        option_layout.addRow('Veri Seç:', image_upload_button)
        option_layout.addRow(self.filename_label, self.image_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(option_layout)
        main_layout.addWidget(send_button)

        central_widget.setLayout(main_layout)

        menubar = QMenuBar()
        self.setMenuBar(menubar)
        profil = menubar.addMenu(f'{self.hasta_adi} {self.hasta_soyadi}')
        profil.addAction('Çıkış', self.close)

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Resim Yükle", "", "Images (*.png *.jpg *.jpeg);"
                                                                            ";All Files (*)", options=options)

        if not file_name:
            return

        if os.path.getsize(file_name) / (1024 * 1024) > 10:
            QMessageBox.warning(self, "Hata", "Resim çok büyük. Lütfen 10 MB'dan küçük bir resim seçin.")
            return

        try:
            if file_name:
                original_image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

                if original_image is not None:
                    resized_image = cv2.resize(original_image, (128, 128))
                    self.display_image(resized_image)

                    self.unique_filename = str(uuid.uuid4()) + '.png'
                    cv2.imwrite('resimler/' + self.unique_filename, resized_image)
                    self.filename_label.setText(f'Yüklenen:')

                    QMessageBox.information(self, "Başarılı", "Resim yüklendi..")
                else:
                    QMessageBox.warning(self, "Hata", "Resim yüklenemedi. Lütfen geçerli bir resim seçin.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Hata oluştu: {str(e)}")

    def display_image(self, image):
        try:
            height, width = image.shape
            bytes_per_line = width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
            self.image_label.setPixmap(QPixmap.fromImage(q_image))
        except Exception as e:
            error_message = f"Hata oluştu: {str(e)}"
            QMessageBox.critical(self, "Hata", error_message)
            QEventLoop(self).exec_()

    def send_data(self):
        try:
            if not self.filename_label.text().strip():
                QMessageBox.warning(self, "Hata", "Resim seçilmedi. Lütfen bir resim seçin.")
                return

            self.image_path = 'resimler/' + self.unique_filename
            insert_into_mrgoruntuleri(sqlite3.connect('hasta_teshis.db'), self.hasta_id, self.selected_option,
                                      self.image_path)

            QMessageBox.information(self, "Başarılı", "Veritabanına kaydedildi.")
            self.clear_image()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Hata oluştu: {str(e)}")

    def clear_image(self):
        self.filename_label.setText('')
        self.image_label.clear()
        self.unique_filename = None


def main():
    app = QApplication(sys.argv)
    ana_sayfa = AnaSayfa(1, '', '')
    ana_sayfa.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
