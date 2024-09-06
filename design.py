# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore,  QtWidgets
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWebEngineWidgets import QWebEngineView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.nextButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.nextButton.setObjectName("nextButton")
        self.gridLayout.addWidget(self.nextButton, 0, 2, 1, 1)

        self.applyPreviousButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.applyPreviousButton.setObjectName("applyPreviousButton")
        self.gridLayout.addWidget(self.applyPreviousButton, 0, 3, 1, 1)


        self.imageViewWidget = QtWidgets.QLabel(parent=self.centralwidget)
        self.imageViewWidget.setScaledContents(True)
        self.imageViewWidget.setMaximumSize(600, 400)
        self.imageViewWidget.setMinimumSize(500,200)
        self.imageViewWidget.setObjectName("imageViewWidget")
        self.gridLayout.addWidget(self.imageViewWidget, 1, 2, 1, 4)

        self.folderSelectButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.folderSelectButton.setObjectName("folderSelectButton")
        self.gridLayout.addWidget(self.folderSelectButton, 0, 0, 1, 1)

        self.fileListWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.fileListWidget.setObjectName("fileListWidget")
        self.gridLayout.addWidget(self.fileListWidget, 1, 0, 2, 2)

        self.previousButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.previousButton.setObjectName("previousButton")
        self.gridLayout.addWidget(self.previousButton, 0, 1, 1, 1)

        self.SaveButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.SaveButton.setObjectName("SaveButton")
        self.gridLayout.addWidget(self.SaveButton, 0, 4, 1, 1)

        self.mapViewWidget = QWebEngineView(parent=self.centralwidget)
        self.imageViewWidget.setMinimumSize(519,251)
        self.mapViewWidget.setGeometry(QtCore.QRect(310, 300, 471, 251))
        self.gridLayout.addWidget(self.mapViewWidget, 2, 2, 1, 4)
        self.create_mapHTLM()

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Photo Location Updater"))
        self.nextButton.setText(_translate("MainWindow", ">"))
        self.applyPreviousButton.setText(_translate("MainWindow", "Apply Previous"))
        self.folderSelectButton.setText(_translate("MainWindow", "Select Folder"))
        self.previousButton.setText(_translate("MainWindow", "<"))
        self.SaveButton.setText(_translate("MainWindow", "Save and next"))
       

    def create_mapHTLM(self):
        """
        Creates an HTML template for a Leaflet map.
        Returns:
        str: The HTML template for the Leaflet map.
        """
        html = """
            <!DOCTYPE html>
                <html>
                <head>
                    <title>Leaflet Map</title>
                    <meta charset="utf-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
                    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
                    <script src="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js"></script>
                    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
                    <link rel="stylesheet" href="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css" />
                    <style>
                        #map { height: 100%; }
                        html, body { height: 100%; margin: 0; }
                    </style>
                </head>
                <body>
                    <div id="map"></div>
                    <script>
                        var map = L.map('map').setView([0, 0], 2);

                        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                            maxZoom: 19,
                            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        }).addTo(map);

                        var geocoder = L.Control.Geocoder.nominatim();
                        L.Control.geocoder({
                            geocoder: geocoder
                        }).addTo(map);

                        var newLocationIcon = L.icon({
                            iconUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAMAAABrrFhUAAADAFBMVEVHcEwAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAEBwAAAAAAAAAAAAABAgAAAQAEBwCb1SiSzSJ3tgui2i2KxxiSzh6m3jJ2tgqm3jNwsAVyrwmo3zSl3TN0tAml3S+FwhWj2y6p4DdjngRurwRrpwdvrQd/vRCGwxWh2i9ppQZQfAVysgZsrgF6uQxbjgV/vhCFwxWq4TldjwZysAmFwxWSzh6i2y08XgOAvhGc1yeZ1CV4twuW0SGRzR6TzyCm3i+n3zKb1SaHxBWFwhSCwBJ2twmt4j+MyRqW0SKs4jx7uw5vsAOPyxyn3jCOyhuY0ySQzB2KxxgjICFsrgGq4Del3S2RzR4pJicmIySU0CCc1ieLyBltrwKIxRdrrQAvLS5xsgVwsQRqrAAwLzCX0iOo4DSg2SqDwRNztAd1tQiu40F0tAhyswaAvhEyMTKd1ygjHyCy5Ut4uAuq4Tmu40O16FQiHh+h2iuz5k226Fap4DWx5UmV0CF/vRBurwN6uQyJxRd+vRB9vA95uAwoJSa46Vuz5k+051Gv5EWf2Cmi2ywsKisuLC2/7mwrKSoWExQqJyg0MzQtKywlISK36Vie2Ck2NTa56l0VExO661++7WiV0CIYFha87GXB73Cw5Eiw5Ec4Nzi762E6OTqSzh/D8HQ9PD2a1CWj3Czt+dUbGBns+NKZ0yS762Pf9LLb8aseGxzq+M3l9sHU75vo98jJ6oHY8aPO7Yvi9brA6W7E8Xjv+djS7pOi2ivF6Xfc8LKe1i23413V7KOo2kO/5XDG8nuz4FSw5Eaj2TO95me75mHK6Iqk2Dut30Ov3ktASijO6ZO54WZabDBqfkGo3TvB5HqHrzCz409MWSyx3lqYwzx/nT1jalJviDY2OySAi2axwY+LrUadxE+q11AUExMrLiCgsXsiIxq+14xJTEKnwmopKxyrwnqNomGWtlWQAAAAAABJmfhmAAABAHRSTlMAEBwfBAkLAQIHIgUaJigPFDIWGC8NERMXFSwZNSo5Px8PD32/nz9l4aTvf4bPXy+/k8FtsS+fT0408fDwfr/P3yjN76+PTt/v39/v7/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8EEjR9jQAAH3pJREFUeNrsm81vWlcaxrub+S9suUVIII/ZZetFIyUamcsGmYVlyQLVZQ0s2GDLjolJlk1qkKqMlFhNahpbkSKI416wCeA7xTcgHAwUsPwxIXaUSEkTZVFppHnPOffj3A/AMyMDzszjRaMqNuf53ed9z3vOdb744v/qpQYGBgb/50wPDRjNBovFjuT3+/F/Ry0Ws3lg5LP3PnjJbDGB7XmQXxIBgUkMG4wDn+2DNxpGwaLsHFOozsoUcCTsDofF/PlFYcQ8jMwRr1Uum2LZp79SYtlENl1ZRQgcSCbDpc8p+MZRO3rE4L2STmz/2kJPnjzZZLNcExOYm/tsGBgtDhLuW1n2yVm0leKWMII50+ULv0UMmk3EPpd69hSrle2nCiXSTURgzmm50D1x0ABPEtzfEt2fVZtPNzdZbh4AOJ2jxgtt32FfS29vihINsolcNs3J4rPZTOLZplq5KhAIhS4mgkHDHPLfzCk9bWey3K0bs7Oz12cl3UBaXV1bq/C5BPlrz9AXKMEhAt6Lh2DIPIf8V1PPRCHzOfB+g5i+LkmGAAiWlpYq2cQzSiyHCHgvWC+4NIr8L2YoI5n0PWRSaZ6GICGA+YjLsfibttAXyyECjGHo4qTf4gT/s7ktIuSev726Suwjv7eVEhmQQlhCCPz+e7ntLVFs1QsETBekDv5kNIH/+bSwfniC6cW9Ndk+9vw9JRGCgEAkAFtnRgCwvZVqehmGsVyEsWDI4gT/txJbAoAMv7S0hvxL9gXf15AoBiKC1bU9kYC9mWXh58DX9nbaAQRM/T8cXjLB1u3P4TVvb29lqvPgfxX7l+1fU0lgIBFYkwg4ltLsNlFiEQj0fSe4HAo5nVVxzanqvMq/5H5REoUAh0BFwDHP4x/HbrPpOYaZGO7nk+LQMPi3p9FqsX2/wr9sf1ElgYEQAmUVwGbq5xMsCwDYzCoQ6ONe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',
                            iconSize: [41, 41],
                            iconAnchor: [20, 41],
                            popupAnchor: [2, -34],
                            shadowUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAApCAQAAAACach9AAACMUlEQVR4Ae3ShY7jQBAE0Aoz/f9/HTMzhg1zrdKUrJbdx+Kd2nD8VNudfsL/Th///dyQN2TH6f3y/BGpC379rV+S+qqetBOxImNQXL8JCAr2V4iMQXHGNJxeCfZXhSRBcQMfvkOWUdtfzlLgAENmZDcmo2TVmt8OSM2eXxBp3DjHSMFutqS7SbmemzBiR+xpKCNUIRkdkkYxhAkyGoBvyQFEJEefwSmmvBfJuJ6aKqKWnAkvGZOaZXTUgFqYULWNSHUckZuR1HIIimUExutRxwzOLROIG4vKmCKQt364mIlhSyzAf1m9lHZHJZrlAOMMztRRiKimp/rpdJDc9Awry5xTZCte7FHtuS8wJgeYGrex28xNTd086Dik7vUMscQOa8y4DoGtCCSkAKlNwpgNtphjrC6MIHUkR6YWxxs6Sc5xqn222mmCRFzIt8lEdKx+ikCtg91qS2WpwVfBelJCiQJwvzixfI9cxZQWgiSJelKnwBElKYtDOb2MFbhmUigbReQBV0Cg4+qMXSxXSyGUn4UbF8l+7qdSGnTC0XLCmahIgUHLhLOhpVCtw4CzYXvLQWQbJNmxoCsOKAxSgBJno75avolkRw8iIAFcsdc02e9iyCd8tHwmeSSoKTowIgvscSGZUOA7PuCN5b2BX9mQM7S0wYhMNU74zgsPBj3HU7wguAfnxxjFQGBE6pwN+GjME9zHY7zGp8wVxMShYX9NXvEWD3HbwJf4giO4CFIQxXScH1/TM+04kkBiAAAAAElFTkSuQmCC',
                            shadowSize: [41, 41],
                            shadowAnchor: [10, 41]
                        });

                        var oldLocationIcon = L.icon({
                            iconUrl: 'data:image/png;base64,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',
                            iconSize: [41, 41],
                            iconAnchor: [20, 41],
                            popupAnchor: [2, -34],
                            shadowUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAApCAQAAAACach9AAACMUlEQVR4Ae3ShY7jQBAE0Aoz/f9/HTMzhg1zrdKUrJbdx+Kd2nD8VNudfsL/Th///dyQN2TH6f3y/BGpC379rV+S+qqetBOxImNQXL8JCAr2V4iMQXHGNJxeCfZXhSRBcQMfvkOWUdtfzlLgAENmZDcmo2TVmt8OSM2eXxBp3DjHSMFutqS7SbmemzBiR+xpKCNUIRkdkkYxhAkyGoBvyQFEJEefwSmmvBfJuJ6aKqKWnAkvGZOaZXTUgFqYULWNSHUckZuR1HIIimUExutRxwzOLROIG4vKmCKQt364mIlhSyzAf1m9lHZHJZrlAOMMztRRiKimp/rpdJDc9Awry5xTZCte7FHtuS8wJgeYGrex28xNTd086Dik7vUMscQOa8y4DoGtCCSkAKlNwpgNtphjrC6MIHUkR6YWxxs6Sc5xqn222mmCRFzIt8lEdKx+ikCtg91qS2WpwVfBelJCiQJwvzixfI9cxZQWgiSJelKnwBElKYtDOb2MFbhmUigbReQBV0Cg4+qMXSxXSyGUn4UbF8l+7qdSGnTC0XLCmahIgUHLhLOhpVCtw4CzYXvLQWQbJNmxoCsOKAxSgBJno75avolkRw8iIAFcsdc02e9iyCd8tHwmeSSoKTowIgvscSGZUOA7PuCN5b2BX9mQM7S0wYhMNU74zgsPBj3HU7wguAfnxxjFQGBE6pwN+GjME9zHY7zGp8wVxMShYX9NXvEWD3HbwJf4giO4CFIQxXScH1/TM+04kkBiAAAAAElFTkSuQmCC',
                            shadowSize: [41, 41],
                            shadowAnchor: [10, 41]
                        });


                        var popup;
                        map.on('click', function(e) {
                            if (popup) {
                                map.closePopup(popup);
                            }
                            popup = L.popup()
                                .setLatLng(e.latlng)
                                .setContent("Location: (" + e.latlng.lat.toString()+ ", " + e.latlng.lng.toString() + ")")
                                .openOn(map);
                            var lat = e.latlng.lat;
                            var lng = e.latlng.lng;
                            new QWebChannel(qt.webChannelTransport, function(channel) {
                                channel.objects.handler.receiveCoordinates(lat, lng);
                            });
                        });

                        // Function to update map location from Python
                        function updateMapLocation(lat, lng, zoom) {
                            map.setView([lat, lng], zoom);
                        }

                        // Function to close the popup
                        function closePopup() {
                            if (popup) {
                                map.closePopup(popup);
                            }
                        }

                        // Expose the function to the QWebChannel
                        window.closePopup = closePopup;

                        // Expose the function to the QWebChannel
                        window.updateMapLocation = updateMapLocation;
                    </script>
                </body>
                </html>
            """
        # Set the HTML content to the mapViewWidget
        self.mapViewWidget.setHtml(html)