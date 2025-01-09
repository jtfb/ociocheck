import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTextEdit, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
import subprocess
import os


class OCIOConfigManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCIO Config Manager")
        self.setGeometry(100, 100, 1000, 600)

        # Main layout with tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Adding tabs
        self.tabs.addTab(self.create_ocio_builder_tab(), "OCIO Builder")
        self.tabs.addTab(self.create_ocio_check_tab(), "OCIO Check")
        self.tabs.addTab(self.create_clf_builder_tab(), "CLF Builder")
        self.tabs.addTab(self.create_lut_builder_tab(), "LUT Builder")
        self.tabs.addTab(self.create_ocio_bake_lut_tab(), "OCIO Bake LUT")

        self.current_config_path = None  # To store the current config path

    def create_ocio_builder_tab(self):
        """Create the OCIO Builder tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        self.config_path_label = QLabel("No OCIO Config loaded.")
        upload_btn = QPushButton("Upload OCIO Config")
        upload_btn.clicked.connect(self.upload_ocio_config)

        self.config_content = QTextEdit()
        self.config_content.setReadOnly(True)

        layout.addWidget(self.config_path_label)
        layout.addWidget(upload_btn)
        layout.addWidget(self.config_content)

        tab.setLayout(layout)
        return tab

    def create_ocio_check_tab(self):
        """Create the OCIO Check tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        self.validation_result = QTextEdit()
        self.validation_result.setReadOnly(True)

        validate_btn = QPushButton("Validate OCIO Config")
        validate_btn.clicked.connect(self.validate_ocio_config)

        layout.addWidget(validate_btn)
        layout.addWidget(self.validation_result)

        tab.setLayout(layout)
        return tab

    def create_clf_builder_tab(self):
        """Create the CLF Builder tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("CLF Builder functionality coming soon."))

        tab.setLayout(layout)
        return tab

    def create_lut_builder_tab(self):
        """Create the LUT Builder tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("LUT Builder functionality coming soon."))

        tab.setLayout(layout)
        return tab

    def create_ocio_bake_lut_tab(self):
        """Create the OCIO Bake LUT tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("OCIO Bake LUT functionality coming soon."))

        tab.setLayout(layout)
        return tab

    def upload_ocio_config(self):
        """Uploads an OCIO configuration file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open OCIO Config", "", "OCIO Config Files (*.ocio)")
        if file_path:
            self.config_path_label.setText(f"OCIO Config Loaded: {file_path}")
            with open(file_path, 'r') as file:
                content = file.read()
                self.config_content.setText(content)
            self.current_config_path = file_path

    def validate_ocio_config(self):
        """Validates the uploaded OCIO configuration using ociocheck."""
        try:
            # Using the specific path for ociocheck in the system
            ocio_check_path = "C:/Users/TIAGOFOA/AppData/Local/Programs/Python/Python311/Scripts/ociocheck.exe"
            result = subprocess.run(
                [ocio_check_path, "-iconfig", self.current_config_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output = result.stdout.decode() + "\n" + result.stderr.decode()
            self.validation_result.setText(output)

            if result.returncode == 0:
                QMessageBox.information(self, "Validation Successful", "OCIO Config is valid!")
            else:
                QMessageBox.warning(self, "Validation Errors", "There were issues with the OCIO Config.")
        except Exception as e:
            self.validation_result.setText(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCIOConfigManager()
    window.show()
    sys.exit(app.exec())
