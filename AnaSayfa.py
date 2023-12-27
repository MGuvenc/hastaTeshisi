import sys

import cv2
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QFormLayout, QComboBox, QFileDialog, QMenuBar, QMainWindow
from PyQt5.QtWidgets import QMessageBox


class AnaSayfa(QMainWindow):
    def __init__(self, hasta_adi, hasta_soyadi):
        super().__init__()

        self.filename_label = None
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
        file_name, _ = QFileDialog.getOpenFileName(self, "Resim Yükle", "",
                                                   "Images (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)

        try:
            if file_name:
                original_image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

                if original_image is not None:
                    resized_image = cv2.resize(original_image, (128, 128))
                    self.display_image(resized_image)
                    self.filename_label.setText(f'Yüklenen:')
                    QMessageBox.information(self, "Başarılı", "Resim yüklendi..")
                else:
                    QMessageBox.warning(self, "Hata", "Resim yüklenemedi. Lütfen geçerli bir resim seçin.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Hata oluştu: {str(e)}")

    def display_image(self, image):
        height, width = image.shape
        bytes_per_line = width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        self.image_label.setPixmap(QPixmap.fromImage(q_image))

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
