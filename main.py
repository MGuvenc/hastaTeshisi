import sys
from PyQt5.QtWidgets import QApplication
from HastaGirisEkrani import HastaGirisEkrani


def main():
    app = QApplication(sys.argv)
    hasta_giris_ekrani = HastaGirisEkrani()
    hasta_giris_ekrani.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
