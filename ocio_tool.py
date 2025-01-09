import os
from PySide2 import QtWidgets

class OCIOTool(QtWidgets.QWidget):
    """Main widget class for the OCIO Tool."""

    def __init__(self):
        """Initialize the OCIO Tool."""
        super().__init__()
        self.setWindowTitle("OCIO Tool")
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        layout = QtWidgets.QVBoxLayout(self)

        # OCIO Configuration tab
        ocio_config_group = QtWidgets.QGroupBox("OCIO Configuration")
        ocio_config_layout = QtWidgets.QVBoxLayout()

        self.ocio_path_label = QtWidgets.QLabel("OCIO Configuration Path:")
        self.ocio_path_entry = QtWidgets.QLineEdit()
        self.ocio_path_entry.setText(os.getenv('OCIO_CONFIG_PATH', ''))

        self.lut_location_label = QtWidgets.QLabel("LUT Location:")
        self.lut_location_entry = QtWidgets.QLineEdit()
        self.lut_location_entry.setText(os.getenv('LUT_LOCATION', ''))

        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(self.save_ocio_configuration)

        ocio_config_layout.addWidget(self.ocio_path_label)
        ocio_config_layout.addWidget(self.ocio_path_entry)
        ocio_config_layout.addWidget(self.lut_location_label)
        ocio_config_layout.addWidget(self.lut_location_entry)
        ocio_config_layout.addWidget(save_button)
        
        ocio_config_group.setLayout(ocio_config_layout)
        layout.addWidget(ocio_config_group)

        # OCIO Bake LUTs tab
        ocio_bake_luts_group = QtWidgets.QGroupBox("OCIO Bake LUTs")
        ocio_bake_luts_layout = QtWidgets.QVBoxLayout()

        ocio_bake_luts_label = QtWidgets.QLabel("OCIO Bake LUTs Options")
        ocio_bake_luts_layout.addWidget(ocio_bake_luts_label)

        ocio_bake_luts_group.setLayout(ocio_bake_luts_layout)
        layout.addWidget(ocio_bake_luts_group)

        self.setLayout(layout)

    def save_ocio_configuration(self):
        """Save the OCIO configuration settings."""
        ocio_config_path = self.ocio_path_entry.text()
        lut_location = self.lut_location_entry.text()

        # Perform actions to save the configuration, e.g., save to a file, set environment variables, etc.
        print("OCIO Configuration Path:", ocio_config_path)
        print("LUT Location:", lut_location)

def main():
    """Main function to run the OCIO Tool."""
    app = QtWidgets.QApplication([])
    ocio_tool = OCIOTool()
    ocio_tool.show()
    app.exec_()

if __name__ == "__main__":
    main()
