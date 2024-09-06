# Photo Location Updater

Photo Location Updater is a PyQt6 application that allows users to update the geolocation metadata of their photos. The application provides a graphical user interface (GUI) to select photos, view their current geolocation, and update the coordinates using a map interface.

## Warning

**Important:** This tool results in the modification data. It is highly recommended to perform a backup of your data before executing the script. The author of this script is not responsible for any data loss or damage that may occur during the execution of this script.

## Features

- Select a folder containing photos.
- Display a list of photos in the selected folder.
- View the current geolocation of a selected photo.
- Update the geolocation of a photo using a map interface.

## Requirements

- Python 3.6+
- ipyleaflet
- ipywidgets 
- piexif 
- PyQt6 
- PyQt6_sip 

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/photo-location-updater.git
   cd photo-location-updater
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. Use the GUI to select a folder containing photos.

3. Select a photo from the list to view its current geolocation.

4. Click on the map to update the geolocation of the selected photo.

5. Save the updated geolocation metadata to the photo.

Alternatively, you can use the following methods to run the application:

- Download the executable file from the [Releases](https://github.com/yourusername/photo-location-updater/releases) tab and run it directly on your system.


## Acknowledgements

This project would not have been possible without the OpenStreetMap:

- [OpenStreetMap](https://www.openstreetmap.org/)


