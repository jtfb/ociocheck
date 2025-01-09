import sys
import os
import subprocess
import xml.etree.ElementTree as ET  # Import for parsing XML files
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QComboBox, QMessageBox
from datetime import datetime

class OCIOConfigManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCIO Config Manager")
        self.setGeometry(100, 100, 1000, 600)

        # Initialize log file path
        self.log_file = "ocio_config_manager.log"

        # Main layout with tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Adding tabs
        self.tabs.addTab(self.create_ocio_builder_tab(), "OCIO Builder")
        self.tabs.addTab(self.create_ocio_check_tab(), "OCIO Check")
        self.tabs.addTab(self.create_clf_builder_tab(), "CLF Builder")
        self.tabs.addTab(self.create_lut_builder_tab(), "LUT Builder")
        self.tabs.addTab(self.create_ocio_bake_lut_tab(), "OCIO Bake LUT")

        # Store last OCIO config path in memory
        self.last_loaded_config = None
        self.colorspaces = []

    def log_action(self, message):
        """Log actions with timestamps to a log file."""
        try:
            with open(self.log_file, "a") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} - {message}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
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

    def upload_ocio_config(self):
        """Uploads an OCIO configuration file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open OCIO Config", "", "OCIO Config Files (*.ocio)")

        if file_path:
            self.config_path_label.setText(f"OCIO Config Loaded: {file_path}")
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.config_content.setText(content)
                self.last_loaded_config = file_path
                self.parse_ocio_config(file_path)
                self.log_action(f"Loaded OCIO config from {file_path}")
            except Exception as e:
                self.log_action(f"Error loading OCIO config: {str(e)}")
                QMessageBox.warning(self, "Error", f"Failed to load OCIO config: {str(e)}")

    def parse_ocio_config(self, config_path):
        """Parse the OCIO config and extract information like color spaces."""
        try:
            tree = ET.parse(config_path)
            root = tree.getroot()

            # Extract colorspaces from the OCIO XML structure
            self.colorspaces = []

            # Assuming color spaces are under the <colorspace> tag (adjust as needed)
            for colorspace in root.findall(".//colorspace"):
                name = colorspace.get('name')
                if name:
                    self.colorspaces.append(name)

            self.log_action(f"Parsed OCIO config with {len(self.colorspaces)} colorspaces")

            # Now update the LUT builder tab with available colorspaces
            self.update_colorspace_dropdowns()

        except ET.ParseError as e:
            self.log_action(f"Error parsing OCIO config: {str(e)}")
            QMessageBox.warning(self, "Error", f"Error parsing OCIO config: {str(e)}")
        except Exception as e:
            self.log_action(f"Error parsing OCIO config: {str(e)}")
            QMessageBox.warning(self, "Error", f"Error parsing OCIO config: {str(e)}")

    def update_colorspace_dropdowns(self):
        """Update the colorspace dropdowns with available color spaces."""
        if hasattr(self, 'input_colorspace_combo') and hasattr(self, 'output_colorspace_combo'):
            self.input_colorspace_combo.clear()
            self.output_colorspace_combo.clear()

            if self.colorspaces:
                self.input_colorspace_combo.addItems(self.colorspaces)
                self.output_colorspace_combo.addItems(self.colorspaces)
            else:
                QMessageBox.warning(self, "Warning", "No colorspaces found in OCIO config.")

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

    def validate_ocio_config(self):
        """Validates the uploaded OCIO configuration using ociocheck."""
        try:
            if self.last_loaded_config:
                result = subprocess.run(
                    ['ociocheck', '-iconfig', self.last_loaded_config],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                output = result.stdout.decode() + "\n" + result.stderr.decode()
                self.validation_result.setText(output)

                if result.returncode == 0:
                    self.log_action("OCIO config validation successful.")
                    QMessageBox.information(self, "Validation Successful", "OCIO Config is valid!")
                else:
                    self.log_action("OCIO config validation failed.")
                    QMessageBox.warning(self, "Validation Errors", "There were issues with the OCIO Config.")
            else:
                QMessageBox.warning(self, "Error", "No OCIO config loaded for validation.")
        except Exception as e:
            self.validation_result.setText(f"Error: {str(e)}")
            self.log_action(f"Error validating OCIO config: {str(e)}")

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

        # Dropdowns for input and output colorspaces
        self.input_colorspace_combo = QComboBox()
        self.output_colorspace_combo = QComboBox()

        # Format dropdown for LUT output
        self.lut_format_combo = QComboBox()
        self.lut_format_combo.addItems(["flame", "3dl", "cube", "spi1d", "csp"])  # Add other formats as needed

        # Add widgets to layout
        layout.addWidget(QLabel("Input Colorspace:"))
        layout.addWidget(self.input_colorspace_combo)
        layout.addWidget(QLabel("Output Colorspace:"))
        layout.addWidget(self.output_colorspace_combo)
        layout.addWidget(QLabel("LUT Format:"))
        layout.addWidget(self.lut_format_combo)

        bake_lut_btn = QPushButton("Bake LUT")
        bake_lut_btn.clicked.connect(self.bake_lut)

        layout.addWidget(bake_lut_btn)

        tab.setLayout(layout)
        return tab

    def bake_lut(self):
        """Bake the LUT based on selected options."""
        input_colorspace = self.input_colorspace_combo.currentText()
        output_colorspace = self.output_colorspace_combo.currentText()
        lut_format = self.lut_format_combo.currentText()

        # Validate selections before attempting to bake
        if not input_colorspace or not output_colorspace or not lut_format:
            QMessageBox.warning(self, "Input Error", "Please select valid input/output colorspaces and LUT format.")
            return

        lut_filename, _ = QFileDialog.getSaveFileName(self, "Save LUT", "", f"{lut_format} Files (*.{lut_format})")
        if not lut_filename:
            return  # If no file selected

        command = f"ociobakelut --input_colorspace {input_colorspace} --output_colorspace {output_colorspace} --format {lut_format} --output {lut_filename}"

        # Log the command and run it
        self.log_action(f"Running command: {command}")

        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode() + "\n" + result.stderr.decode()
            if result.returncode == 0:
                self.log_action("LUT baked successfully.")
                QMessageBox.information(self, "LUT Creation Successful", "LUT baked successfully!")
            else:
                self.log_action("Error baking LUT.")
                QMessageBox.warning(self, "Error", f"Error creating LUT: {output}")
        except Exception as e:
            self.log_action(f"Error baking LUT: {str(e)}")
            QMessageBox.warning(self, "Error", f"Error creating LUT: {str(e)}")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCIOConfigManager()
    window.show()
    sys.exit(app.exec())
