from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel,QApplication


class ContactDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()

        version = QLabel("App Information:\nBuilt by: Rick45\nVersion: 1.2.1")
        layout.addWidget(version)
        
        # Add a QLabel with a clickable URL
        url_label = QLabel('Github <a href="https://github.com/Rick45/photo-location-updater">Photo Location Updater</a>')
        url_label.setOpenExternalLinks(True)  # Enable opening links in the default web browser
        layout.addWidget(url_label)
        
        self.setLayout(layout)
        # Center the dialog on the screen
        self.center()

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        dialog_geometry = self.frameGeometry()
        dialog_geometry.moveCenter(screen_geometry.center())
        self.move(dialog_geometry.topLeft())