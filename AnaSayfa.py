from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel
import sys


class AnaSayfa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('AnaSayfa')
        layout = QVBoxLayout()
        label = QLabel('Hoş geldin!')
        layout.addWidget(label)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)
    ana_sayfa = AnaSayfa()
    ana_sayfa.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()