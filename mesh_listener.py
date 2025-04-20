import meshtastic
import meshtastic.serial_interface
from pubsub import pub
import time
import csv
import os

encodedMessageLength = 44

seen_messages = set()
decodedMessage = ""

def onReceive(packet, interface=None):
    decoded = packet.get("decoded", {})
    from_id = packet.get("fromId", "unknown")

    if "text" in decoded:
        message = decoded["text"]
        if message not in seen_messages:
            seen_messages.add(message)
            print(f"Message received from {from_id}: {message}")
            decode_weather_packet(message)


csv_file = "weather_log.csv"

if not os.path.exists(csv_file):
    with open(csv_file, mode = 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature (C)", "Humidity (%)", "Pressure (hPa)", "Latitude", "Longitude", "Altitude (m)"])

def decode_weather_packet(message):
    if len(message) < encodedMessageLength:
        print("your message is too short, stupid: ", message)
        return
    
    try:
        # weather
        temp = int(message[0:4]) / 100
        hum = int(message[4:8]) / 100
        pres = int(message[8:12]) / 10
        time_str = message[38:44]
        timestamp = f"{time_str[0:2]}:{time_str[2:4]}:{time_str[4:6]}"

        # gps
        lat_sign = -1 if message[12] == '1' else 1
        lat_val = int(message[13:21]) / 1e5
        latitude = lat_sign * lat_val

        lon_sign = -1 if message[21] == '1' else 1
        lon_val = int(message[22:31]) / 1e6
        longitude = lon_sign * lon_val

        altitude = int(message[31:38]) / 1000


        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, f"{temp:.2f}", f"{hum:.2f}", f"{pres:.1f}", f"{latitude:.5f}", f"{longitude:.5f}", f"{altitude:.3f}"])

        print(f"Logged: {timestamp}, Temp: {temp:.2f} °C, Humidity: {hum:.2f} %, Pressure: {pres:.1f} hPa, Lat: {latitude:.5f}, Lon: {longitude:.5f}, Alt: {altitude:.3f} m")

    except ValueError as e:
        print("Failed to decode message :[ {message}")
        print(f"Error: {e}")

# Subscribe to all incoming packets
pub.subscribe(onReceive, "meshtastic.receive")

# Open connection to the radio
iface = meshtastic.serial_interface.SerialInterface()

# Keep the script running
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting due to keyboard interrupt")