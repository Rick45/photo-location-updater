# Photo Location Updater

Photo Location Updater is a PyQt6 application that allows users to update the geolocation metadata of their photos. The application provides a graphical user interface (GUI) to select photos, view their current geolocation, and update the coordinates using a map interface.

## Warning

**Important:** This tool results in data modification. It is highly recommended that a data backup be performed before executing the script. The script's author is not responsible for any data loss or damage that may occur during the execution of this script.

## Features

- Select a folder containing photos.
- Display a list of photos in the selected folder.
- View the current geolocation of a selected photo.
- Update the geolocation of a photo using a map interface.

![app](./src/sample.png)



## App Execution 

There are two ways to run the app.

1. By download the executable and run it directly on your system. **Important:** that the windows could say the app is unverified.

2. By downloading this repository and run it from the source code.



## Execution with .exe

1. Download the executable file from the [Releases](https://github.com/Rick45/photo-location-updater/releases) tab.

2. Extracto to your desired folder **Important:** you need to extract all the content(both EXE and folder).

3. Run the "Photo Location Updater.exe" file


## Execution by source code

### Requirements

- Python 3.6+

### Installation

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

4. Run the application:
    ```sh
    python main.py
    ```


## App Usage

1. Use the GUI to select a folder containing photos.

2. Select a photo from the list to view its current geolocation.

3. Click on the map to update the geolocation of the selected photo.

4. Save the updated geolocation metadata to the photo.


## Acknowledgements

This project would not have been possible without the OpenStreetMap:

- [OpenStreetMap](https://www.openstreetmap.org/)


## Thanks
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/rick45)
