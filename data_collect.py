import serial
import os
from datetime import datetime

# === USER INPUT ===
label = input("Enter label for this recording: ")
folder_name = f"data/label_{label}"

# === CONFIG ===
serial_port = 'COM5'
baud_rate = 115200
lines_per_packet = 500 * 1.5  # 500Hz for 2 second

# === SETUP ===
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

ser = serial.Serial(serial_port, baud_rate)
print(f"Listening on {serial_port}... Waiting for packet.")

buffer = []

try:
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if "ready" in line:
            buffer = []  # clear buffer when ESP32 is ready
            continue
        if not line or len(line.split(",")) != 6:
            continue

        buffer.append(line)

        # If 1.5 second of data collected
        if len(buffer) >= lines_per_packet:
            print("1.5 second of data collected. Saving to file...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(folder_name, f"{timestamp}.txt")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(buffer))

            print(f"Saved packet to: {file_path}")
            buffer = []  # clear for next packet

except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    ser.close()
