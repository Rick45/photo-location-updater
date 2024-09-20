import json
from datetime import datetime, timezone
import re

def parse_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    timeline_objects = data.get("timelineObjects", [])
    extracted_data = []

    for obj in timeline_objects:
        if "activitySegment" in obj:
            activity_segment = obj["activitySegment"]
            start_location = activity_segment.get("startLocation", {})
            start_timestamp = activity_segment.get("duration", {}).get("startTimestamp", "")
            
            if start_location and start_timestamp:
                latitude = start_location.get("latitudeE7", 0) / 1e7
                longitude = start_location.get("longitudeE7", 0) / 1e7
                extracted_data.append({
                    "DateTime": start_timestamp,
                    "Latitude": latitude,
                    "Longitude": longitude
                })

    return extracted_data

def get_closest_location(data, target_timestamp):
    closest_location = None
    closest_distance = float("inf")
    distance = 0
    for entry in data:
        entry_timestamp = entry["DateTime"]
        entry_datetime = None
        # for some reason google have two different timestamp formats
        timestamp_format_A = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
        timestamp_format_B = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$')
        
        if timestamp_format_A.match(entry_timestamp):            
            entry_datetime = datetime.strptime(entry_timestamp, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        elif timestamp_format_B.match(entry_timestamp):
            entry_datetime = datetime.strptime(entry_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        else:
            print(f"Invalid timestamp format: {entry_timestamp}")
            continue
        target_datetime = datetime.strptime(target_timestamp, '%Y:%m:%d %H:%M:%S').replace(tzinfo=timezone.utc)
        distance = abs((entry_datetime - target_datetime).total_seconds())
        if distance < closest_distance:
            closest_distance = distance
            closest_location = entry

    distanceInMinutes = closest_distance / 60
    if closest_location:
        return closest_location["Latitude"], closest_location["Longitude"], distanceInMinutes
    else:
        return None, None, None

if __name__ == "__main__":
    file_path = "2024_AUGUST.json"
    data = parse_json_file(file_path)
    for entry in data:
        print(entry)