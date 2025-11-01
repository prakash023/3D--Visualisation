"""
Simple ISS Location Tracker
Gets current International Space Station position and saves to CSV file
Created for learning purposes
Date started: 2025-11-01
"""

import requests
import time
import csv
import os
from datetime import datetime

# Where to save the data file
folder_path = r"E:\QGIS\ne_10m_land\Datasets_contour\30_dayChallenge\Day_01_Points"
file_name = "ISS_track.csv"
full_file_path = os.path.join(folder_path, file_name)

# Create folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# List to store all the location data
location_data = []

print("Starting ISS tracker...")
print("Getting ISS position every 60 seconds")
print("Press Ctrl+C to stop the program")
print()

try:
    while True:
        try:
            # Get data from the ISS API
            response = requests.get("https://api.wheretheiss.at/v1/satellites/25544")
            
            # Check if request was successful
            if response.status_code == 200:
                iss_data = response.json()
                
                # Convert timestamp to readable date/time
                timestamp = iss_data["timestamp"]
                readable_time = datetime.utcfromtimestamp(timestamp)
                time_string = readable_time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Get the position information
                lat = iss_data["latitude"]
                lon = iss_data["longitude"]
                alt = iss_data["altitude"]
                speed = iss_data["velocity"]
                
                # Create a dictionary for this reading
                current_location = {
                    "timestamp": time_string,
                    "latitude": lat,
                    "longitude": lon,
                    "altitude_km": alt,
                    "velocity_km_h": speed
                }
                
                # Add to our data list
                location_data.append(current_location)
                
                # Write to CSV file
                with open(full_file_path, 'w', newline='') as csvfile:
                    fieldnames = ['timestamp', 'latitude', 'longitude', 'altitude_km', 'velocity_km_h']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    # Write header only if file is empty
                    if csvfile.tell() == 0:
                        writer.writeheader()
                    
                    # Write all data rows
                    for location in location_data:
                        writer.writerow(location)
                
                # Print current position to screen
                print(f"Time: {time_string}")
                print(f"Position: {lat:.3f}°N, {lon:.3f}°E")
                print(f"Altitude: {alt:.1f} km")
                print(f"Speed: {speed:.1f} km/h")
                print("-" * 50)
                
            else:
                print(f"Error: Could not get data (Status code: {response.status_code})")
            
            # Wait 60 seconds before next check
            time.sleep(60)
            
        except requests.exceptions.ConnectionError:
            print("Network error - check internet connection")
            time.sleep(60)
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            time.sleep(60)
        except KeyError as e:
            print(f"Data format error - missing field: {e}")
            time.sleep(60)
            
except KeyboardInterrupt:
    print("\nStopping ISS tracker...")
    print(f"Collected {len(location_data)} location points")
    print(f"Data saved to: {full_file_path}")