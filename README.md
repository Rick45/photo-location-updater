![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/github/license/Rick45/photo-location-updater)

# Photo Location Updater
A simple tool to seamlessly update the geolocation metadata of your photos using an intuitive map-based interface. Whether you need to correct or add location data, this app makes it easy.


## Warning

**Important:** This tool results in data modification. It is highly recommended that a data backup be performed before executing the script. The script's author is not responsible for any data loss or damage that may occur during the execution of this script.

## Features
- 📂 Select a folder containing photos
- 🌍 View and update photo geolocation on an interactive map
- 🤖 Automate geolocation updates using Google Takeout data
- 💾 Save updated metadata easily


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

## Installation (via source)
1. Clone the repository:
    ```bash
    git clone https://github.com/Rick45/photo-location-updater.git
    ```
2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate     # On Windows
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the app:
    ```bash
    python main.py
    ```

## App Usage

1. Use the GUI to select a folder containing photos.

2. Select a photo from the list to view its current geolocation.

3. Click on the map to update the geolocation of the selected photo.

4. Save the updated geolocation metadata to the photo.

Optionally you can load the google takeout files using the Load Google Takeout button. When a file from the list is selected the app will use it to find the location with the date closest the photo taken date. Google share the location history by month, so you will need to know the month where the photo was taken.



## How to Request Location Data from Google Takeout

1. Go to Google Takeout: Visit Google Takeout and sign in with your Google account.

2. Select Data to Include:

3. Click on "Deselect all" to clear all selections.
4. Scroll down and find "Location History".
5. Check the box next to "Location History".
6. Choose File Type, Frequency & Destination:

7. Click on "Next step".
8. Choose the delivery method,export frequency, file type and size.
9. Click on "Create export".

Google will prepare your data, which may take some time depending on the amount of data.
Once the export is ready, you will receive an email with a download link.
Download the .zip file and extract it to a folder on your computer.
This folder can be selected and all the files will be listed in the aplication to be selected.


## Acknowledgements

This project would not have been possible without the OpenStreetMap:

- [OpenStreetMap](https://www.openstreetmap.org/)


## Thanks
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/rick45)
