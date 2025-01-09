import sys
from PyQt6.QtWidgets import QApplication, QWidget

try:
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Minimal Window Test")
    window.resize(400, 300)
    window.show()
    print("Window should be visible.")
    app.exec()
except Exception as e:
    print(f"Error: {e}")
