import sys

from PySide6.QtWidgets import QApplication

from gui.MainWindow import MainWindow


def main():
    #inicia o lop da gui
    app = QApplication(sys.argv)

    window = MainWindow()#inicia a janela
    window.show()#mosta a janela

    sys.exit(app.exec())


if __name__ == "__main__":
    main()