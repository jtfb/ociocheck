import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTextEdit, QFileDialog, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
import subprocess
import PyOpenColorIO as OCIO

class OCIOConfigManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCIO Config Manager")
        self.setGeometry(100, 100, 1000, 600)

        # Initialize colorspaces as an empty list
        self.colorspaces = []

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

        # Initialize the combo boxes for colorspaces
        self.input_colorspace_combo = QComboBox()
        self.output_colorspace_combo = QComboBox()

        # Add all colorspaces available after loading the OCIO config
        self.input_colorspace_combo.addItems(self.colorspaces)
        self.output_colorspace_combo.addItems(self.colorspaces)

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
            # Load the OCIO config using PyOCIO
            config = OCIO.Config.CreateFromFile(config_path)

            # Retrieve all colorspaces
            self.colorspaces = [cs.getName() for cs in config.getColorSpaces()]

            # Update the combo boxes with loaded colorspaces
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

        if lut_format not in ["flame", "3dl", "cube", "spi1d", "csp", "houdini"]:
            QMessageBox.warning(self, "LUT Format Error", "Invalid LUT format selected.")
            return

        try:
            # Path to ociobakelut executable
            ocio_bakelut_path = "C:/Users/TIAGOFOA/AppData/Local/Programs/Python/Python311/Scripts/ociobakelut.exe"
            
            # Open save file dialog with default extension based on LUT format
            output_file, _ = QFileDialog.getSaveFileName(self, "Save LUT File", "", f"{lut_format.upper()} Files (*.{lut_format})")
            
            if output_file:
                # Check if the user has selected a valid path
                if not os.path.exists(os.path.dirname(output_file)):
                    os.makedirs(os.path.dirname(output_file))

                # Ensure the file extension is added if not present
                if not output_file.lower().endswith(f".{lut_format.lower()}"):
                    output_file += f".{lut_format}"

                # Verify if the file exists and prompt the user
                if os.path.exists(output_file):
                    confirm = QMessageBox.question(self, "File Exists", f"File already exists: {output_file}. Do you want to overwrite?",
                                                QMessageBox.Yes | QMessageBox.No)
                    if confirm == QMessageBox.No:
                        return  # If the user chooses No, we don't proceed.

                # Construct the ociobakelut command
                command_args = [
                    ocio_bakelut_path,
                    "--format", lut_format,
                    "--inputspace", input_colorspace,
                    "--outputspace", output_colorspace,
                    "--output", output_file
                ]

                print(f"Command being executed: {command_args}")  # Debugging: Log the command
                print(f"Saving LUT to: {output_file}")  # Debugging: Log the file path

                # Run the subprocess to generate the LUT
                result = subprocess.run(command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
