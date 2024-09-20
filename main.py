import os
import sys
from metadataHandler import get_image_metadata, apply_metadata_to_image
from locationHistoryLoader import parse_json_file, get_closest_location
from design import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QMessageBox, QTreeWidgetItem
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtGui import QPixmap, QImageReader
from PyQt6.QtWebEngineWidgets import QWebEngineView
from contactDialog import *

#global vars
selectedCoordinates = None
previousCoordinates = None
originalCoordinates = None
takeOutData = None

class Handler(QObject):
    coordinates_received = pyqtSignal(float, float)

    @pyqtSlot(float, float)
    def receiveCoordinates(self, lat, lng):
        self.coordinates_received.emit(lat, lng)

#.\photoLocationUpdaterEnv\Scripts\activate
class Window(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        QImageReader.setAllocationLimit(0)

        # Set up the QWebChannel
        self.channel = QWebChannel()
        self.handler = Handler()
        self.channel.registerObject('handler', self.handler)
        self.mapViewWidget.page().setWebChannel(self.channel)


        self.gpsFilesListWidget.hide()
        self.clearGoogleTakeOutButton.hide()

        self.folderSelectButton.clicked.connect(self.select_folder)

        self.handler.coordinates_received.connect(self.handle_coordinates)

        self.SaveButton.clicked.connect(self.handle_saveButton)

        self.applyPreviousButton.clicked.connect(self.handle_applyPreviousButton)

        self.nextButton.clicked.connect(self.handle_nextButton)
        self.previousButton.clicked.connect(self.handle_previousButton)
        
        self.actionAbout.triggered.connect(self.show_contact_info)

        
        self.googleTakeOutButton.clicked.connect(self.select_folderTakeOutFile)

        self.clearGoogleTakeOutButton.clicked.connect(self.select_clearTakoutFile)
        ##############################image
        
        # Connect the item click event to a method
        self.fileListWidget.itemClicked.connect(self.show_image)

        self.gpsFilesListWidget.itemClicked.connect(self.loadTakeOutFile)

    def select_clearTakoutFile(self):
        global takeOutData
        takeOutData = None
        self.gpsFilesListWidget.hide()
        self.gpsFilesListWidget.clear()        
        self.clearGoogleTakeOutButton.hide()
        self.createAlert("Takeout file cleared, no location will be calculated from the takeout file")


    def show_contact_info(self):
            dialog = ContactDialog()
            dialog.exec()


    def handle_previousButton(self):
        """
        Handles the action when the previous button is clicked.

        Retrieves the current row from the fileListWidget and checks if it is valid.
        If the current row is valid, it sets the previous row as the current row and shows the image associated with the current item.
        If the current row is not valid, it sets the last row as the current row and shows the image associated with the current item.
        """
        current_row = self.fileListWidget.currentRow()
        if current_row == -1:
            return
        previous_row = current_row - 1
        if previous_row >= 0:
            self.fileListWidget.setCurrentRow(previous_row)
            self.show_image(self.fileListWidget.currentItem())
        else:
            self.fileListWidget.setCurrentRow(self.fileListWidget.count() - 1)
            self.show_image(self.fileListWidget.currentItem())

    def handle_nextButton(self):
        """
        Handles the action when the next button is clicked.

        Retrieves the current row from the fileListWidget and increments it by 1.
        If the next row is within the range of the fileListWidget count, sets the current row to the next row and shows the image of the current item.
        If the next row is outside the range, sets the current row to 0 (first item) and shows the image of the current item.
        """
        current_row = self.fileListWidget.currentRow()
        if current_row == -1:
            return
        next_row = current_row + 1
        if next_row < self.fileListWidget.count():
            self.fileListWidget.setCurrentRow(next_row)
            self.show_image(self.fileListWidget.currentItem())
        else:
            self.fileListWidget.setCurrentRow(0) # Go back to the first item
            self.show_image(self.fileListWidget.currentItem())


    def handle_applyPreviousButton(self):
        """
        Handles the event when the "Apply Previous" button is clicked.
        This function updates the selected coordinates with the previous coordinates if they exist.
        It removes any existing markers from the map and adds new markers for the previous and original coordinates.
        It also updates the map location to center around the previous coordinates.
        If there are no previous coordinates, it displays an alert message.
        """
        global selectedCoordinates
        global previousCoordinates
        global originalCoordinates
        if previousCoordinates != None:
            selectedCoordinates = previousCoordinates
            self.mapViewWidget.page().runJavaScript("map.eachLayer(function(layer) { if (layer instanceof L.Marker) { map.removeLayer(layer); } });")
            self.mapViewWidget.page().runJavaScript("closePopup();")

            self.mapViewWidget.page().runJavaScript(f"L.marker([{previousCoordinates[0]},{previousCoordinates[1]}], {{icon: newLocationIcon}}).addTo(map).bindPopup('New Location: Latitude = {previousCoordinates[0]}, Longitude = {previousCoordinates[1]}');")  # Add marker to the map with info
            self.mapViewWidget.page().runJavaScript(f"L.marker([{originalCoordinates[0]},{originalCoordinates[1]}], {{icon: oldLocationIcon}}).addTo(map).bindPopup('Original Location: Latitude = {originalCoordinates[0]}, Longitude = {originalCoordinates[1]}');")  # Add marker to the map with info
            

            self.mapViewWidget.page().runJavaScript(f"updateMapLocation({previousCoordinates[0]}, {previousCoordinates[1]}, 15);")
  
        else:
            self.createAlert("No Previous Coordinates to apply")

    def createAlert(self, message):
        """
        Display a warning alert with the given message.

        Parameters:
        - message (str): The message to be displayed in the alert.

        Returns:
        - None
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle("Alert")
        msg.exec()

    def handle_saveButton(self):
        """
        Handles the save button action.
        This method is responsible for saving the selected image's metadata. It checks if an image is selected, and if not, it displays an alert message. If coordinates are selected, it updates the metadata with the selected coordinates and applies the metadata to the image. If no coordinates are selected, it displays an alert message. Finally, it resets the selected coordinates and calls the next button action.
        Parameters:
        - self: The current instance of the class.
        Returns:
        - None
        """
        current_row = self.fileListWidget.currentRow()
        if current_row == -1:
            self.createAlert("No image selected")
            return
        global selectedCoordinates
        global previousCoordinates
        metadata = {}
        if selectedCoordinates != None:
            previousCoordinates = selectedCoordinates
            metadata['GPSLatitude'] = selectedCoordinates[0]
            metadata['GPSLongitude'] = selectedCoordinates[1]
            imagePath = self.fileListWidget.currentItem().data(1)
            apply_metadata_to_image(imagePath,metadata)            
        else:
            self.createAlert("No Coordinates selected")
            return
        
        #call next button
        selectedCoordinates= None
        self.handle_nextButton()


    @pyqtSlot(float, float)
    def handle_coordinates(self, lat, lng):
        global selectedCoordinates
        selectedCoordinates = (lat, lng)


    def select_folder(self):
        """
        Opens a file dialog to select a folder and displays its path.
        If a folder was selected, it calls the `list_photos` method to list photo files in the selected folder.
        Returns:
            None
        """
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')

        # If a folder was selected, display its path and list photo files
        if folder_path:
            self.list_photos(folder_path)

    def list_photos(self, folder_path):
        """
        List all photo files in the selected folder and display them in the file list widget.
        Parameters:
        - folder_path (str): The path of the folder containing the photos.
        Returns:
        None
        """
        # Clear the fileListView before adding new items
        self.fileListWidget.clear()

        # List all photo files in the selected folder
        photo_extensions = ('.jpg', '.jpeg', '.tiff')
        firstfile = None
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(photo_extensions):
                item = QListWidgetItem(file_name)
                item.setData(1, os.path.join(folder_path, file_name))  # Store the full path
                if firstfile == None:
                    firstfile = item
                self.fileListWidget.addItem(item)
        
        # Show the first image in the image view widget
        if firstfile != None:
            self.fileListWidget.setCurrentRow(0)
            self.show_image(firstfile)

    def show_image(self, item):
        """
        Display the selected image in the image view widget and set its location on the map.
        Parameters:
        - item: The item representing the selected image.
        Returns:
        None
        """
        # Get the full path of the selected image
        image_path = item.data(1)
        pixmap = QPixmap(image_path)
        self.imageViewWidget.setPixmap(pixmap)
        self.imageViewWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image

        ##logic to show image in map
        metadata = get_image_metadata(image_path)
        if(metadata.__len__() == 1 and 'CreatedDate' in metadata and takeOutData != None):
            self.set_image_aproximated_location(metadata)
            return
        else:
            self.set_image_location(metadata)

    def set_image_location(self, metadata):
        """
        Sets the image location on the map based on the provided metadata.

        Parameters:
        - metadata: A dictionary containing the metadata of the image.

        Returns:
        None
        """
        # Remove all existing markers
        self.mapViewWidget.page().runJavaScript("map.eachLayer(function(layer) { if (layer instanceof L.Marker) { map.removeLayer(layer); } });")
        self.mapViewWidget.page().runJavaScript("closePopup();")
        global originalCoordinates
        # Set the image location on the map
        if 'GPSLatitude' in metadata and 'GPSLongitude' in metadata:
            lat = metadata['GPSLatitude']
            lng = metadata['GPSLongitude']
            originalCoordinates= (lat, lng)
            self.mapViewWidget.page().runJavaScript(f"updateMapLocation({lat}, {lng}, 15);")
            jscode = str(f"L.marker([{lat},{lng}], {{icon: newLocationIcon}}).addTo(map).bindPopup('Location: Latitude = {lat}, Longitude = {lng}');")
            self.mapViewWidget.page().runJavaScript(jscode)  # Add marker to the map with info
        else:
            self.mapViewWidget.page().runJavaScript(f"updateMapLocation(0, 0, 2);")


    def set_image_aproximated_location(self, metadata):
        closestLocation = get_closest_location(takeOutData, metadata['CreatedDate'])
        if closestLocation[0] == None:
            return
        else:
            # Remove all existing markers
            self.mapViewWidget.page().runJavaScript("map.eachLayer(function(layer) { if (layer instanceof L.Marker) { map.removeLayer(layer); } });")
            self.mapViewWidget.page().runJavaScript("closePopup();")
            global selectedCoordinates
            # Set the image location on the map
            lat = closestLocation[0]
            lng = closestLocation[1]
            selectedCoordinates = (lat, lng)
            distanceInMinutes = round(closestLocation[2], 2)
            self.mapViewWidget.page().runJavaScript(f"updateMapLocation({lat}, {lng}, 15);")
            hours, minutes = divmod(distanceInMinutes, 60)
            jscode = str(f"L.marker([{lat},{lng}], {{icon: calculatedLocation}}).addTo(map).bindPopup('Calculated location have {int(hours):02d}H{int(minutes):02d}M difference from the photo date');")
            self.mapViewWidget.page().runJavaScript(jscode)


    def select_folderTakeOutFile(self):
        # Clear the fileListView before adding new items
        self.clearGoogleTakeOutButton.show()
        self.gpsFilesListWidget.show()
        self.gpsFilesListWidget.clear()
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        # List all photo files in the selected folder
        files_extensions = ('.json')
        firstfile = None

        for root, dirs, files in os.walk(folder_path):
            json_files = [file_name for file_name in files if file_name.lower().endswith(files_extensions)]
            if json_files:
                parent_item = QTreeWidgetItem(self.gpsFilesListWidget, [os.path.basename(root)])
                for file_name in json_files:
                    item = QTreeWidgetItem(parent_item, [file_name])
                    item.setData(0, Qt.ItemDataRole.UserRole, root+'/'+file_name)  # Store the full path
                    if firstfile is None:
                        firstfile = item
        
    def loadTakeOutFile(self, item, column):

        global takeOutData
        
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        #file_path = QFileDialog.getOpenFileName(self, 'Select Takeout File', '', 'JSON Files (*.json)')
        if file_path:
            try:
                takeOutData = parse_json_file(file_path)
                current_row = self.fileListWidget.currentRow()
                self.show_image(self.fileListWidget.currentItem())
                self.createAlert("Takeout file loaded successfully, if there is no location metadata in the photo, the system will use the takeout data to get the closest location for the photo created date")
            except:
                self.createAlert("Invalid Takeout file")

        else:
            self.createAlert("No no file selected nothing will be processed")
            return

        


app = QApplication(sys.argv)
window = Window()

app.setStyle("Fusion")
window.show()
app.exec()