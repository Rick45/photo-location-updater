import piexif

patternForDecimals = r"\(\s*\d+\s*,\s*\d+\s*\)"

def get_image_metadata(image_path):
    exif_dict = piexif.load(image_path)
    metadata = {}
    latitudeRef = None
    longitudeRef = None
    latitude = None
    longitude = None
    created_date = None

    if exif_dict['GPS'] != {}:
        latitudeRef = str(exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef])
        longitudeRef = str(exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef])
        latitude = exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]
        longitude = exif_dict['GPS'][piexif.GPSIFD.GPSLongitude]

    if exif_dict['Exif'] != {}:
        created_date = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)

    if latitudeRef and longitudeRef and latitude and longitude:
        metadata = convert_to_decimal(latitudeRef, longitudeRef, latitude, longitude)

    if created_date:
        metadata['CreatedDate'] = created_date.decode('utf-8') if isinstance(created_date, bytes) else created_date

    return metadata

def convert_to_decimal(latitudeRef, longitudeRef, latitude, longitude):
    metadata = {}
    if latitudeRef and longitudeRef and latitude and longitude:
        metadata['GPSLatitude'] = dms_to_decimal(latitude[0][0]/latitude[0][1], latitude[1][0]/latitude[1][1], latitude[2][0]/latitude[2][1])
        metadata['GPSLongitude'] = dms_to_decimal(longitude[0][0]/longitude[0][1], longitude[1][0]/longitude[1][1], longitude[2][0]/longitude[2][1])
        if "S" in latitudeRef or "W" in latitudeRef:
            metadata['GPSLatitude'] = -metadata['GPSLatitude']
        if "S" in longitudeRef or "W" in longitudeRef:
            metadata['GPSLongitude'] = -metadata['GPSLongitude']
    return metadata


def dms_to_decimal(degrees, minutes, seconds):
    return degrees + (minutes / 60) + (seconds / 3600) 

def apply_metadata_to_image(image_path, metadata):
    exif_dict = piexif.load(image_path)
    
    latitude = metadata.get('GPSLatitude')
    longitude = metadata.get('GPSLongitude')
    
    if latitude and longitude:
        # Convert latitude and longitude from decimal degrees to EXIF format
        lat_d, lat_m, lat_s, lat_positive = decimal_degrees_to_dms(latitude)
        lon_d, lon_m, lon_s, lon_positive = decimal_degrees_to_dms(longitude)

        # Format for EXIF
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = [(lat_d, 1), (lat_m, 1), (int(lat_s * 100), 100)]
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = 'N' if lat_positive else 'S'
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = [(lon_d, 1), (lon_m, 1), (int(lon_s * 100), 100)]
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = 'E' if lon_positive else 'W'
    
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)
            
def decimal_degrees_to_dms(degrees):
	is_positive = degrees >= 0
	degrees = abs(degrees)
	d = int(degrees)
	m = int((degrees - d) * 60)
	s = (degrees - d - m/60) * 3600.0
	return d, m, s, is_positive