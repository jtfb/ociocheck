import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTextEdit, QFileDialog, QComboBox, QMessageBox
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
        self.colorspaces = []  # To store the available colorspaces

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

        # Widgets for selecting input/output colorspaces and LUT format
        self.input_colorspace_combo = QComboBox()
        self.output_colorspace_combo = QComboBox()
        self.lut_format_combo = QComboBox()
        self.lut_format_combo.addItems(["flame", "3dl", "cube", "spi1d", "csp"])

        bake_lut_btn = QPushButton("Bake LUT")
        bake_lut_btn.clicked.connect(self.bake_lut)

        layout.addWidget(QLabel("Input Colorspace:"))
        layout.addWidget(self.input_colorspace_combo)
        layout.addWidget(QLabel("Output Colorspace:"))
        layout.addWidget(self.output_colorspace_combo)
        layout.addWidget(QLabel("LUT Format:"))
        layout.addWidget(self.lut_format_combo)
        layout.addWidget(bake_lut_btn)

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
            self.load_colorspaces(file_path)

    def load_colorspaces(self, config_path):
        """Load the available colorspaces from the OCIO config file."""
        try:
            # Parse the OCIO config file and extract the colorspaces
            # This is a simple placeholder. Modify it to suit the actual structure of the OCIO config.
            ocio_check_path = "C:/Users/TIAGOFOA/AppData/Local/Programs/Python/Python311/Scripts/ociocheck.exe"
            result = subprocess.run(
                [ocio_check_path, "-iconfig", config_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output = result.stdout.decode() + "\n" + result.stderr.decode()

            # Extracting colorspaces from the config (placeholder, adapt as needed)
            if "ColorSpace" in output:
                self.colorspaces = ["ACES", "Rec.709", "sRGB"]  # Modify this as per the output structure
                self.input_colorspace_combo.clear()
                self.output_colorspace_combo.clear()
                self.input_colorspace_combo.addItems(self.colorspaces)
                self.output_colorspace_combo.addItems(self.colorspaces)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load colorspaces: {str(e)}")

    def bake_lut(self):
        """Bake the LUT using ociobakelut."""
        input_colorspace = self.input_colorspace_combo.currentText()
        output_colorspace = self.output_colorspace_combo.currentText()
        lut_format = self.lut_format_combo.currentText()

        if not input_colorspace or not output_colorspace:
            QMessageBox.warning(self, "Input Error", "Please select both input and output colorspaces.")
            return

        if lut_format not in ["flame", "3dl", "cube", "spi1d", "csp"]:
            QMessageBox.warning(self, "LUT Format Error", "Invalid LUT format selected.")
            return

        try:
            # Call the ociobakelut command
            ocio_bakelut_path = "C:/Users/TIAGOFOA/AppData/Local/Programs/Python/Python311/Scripts/ociobakelut.exe"
            output_file = QFileDialog.getSaveFileName(self, "Save LUT File", "", f"{lut_format} Files (*.{lut_format})")[0]
            if output_file:
                result = subprocess.run(
                    [ocio_bakelut_path, "-i", input_colorspace, "-o", output_colorspace, "-f", lut_format, "-o", output_file],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )

                output = result.stdout.decode() + "\n" + result.stderr.decode()
                if result.returncode == 0:
                    QMessageBox.information(self, "LUT Baking Success", f"LUT saved to: {output_file}")
                else:
                    QMessageBox.warning(self, "LUT Baking Error", f"Error: {output}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to bake LUT: {str(e)}")

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
