import os
import serial
import numpy as np
from tensorflow.keras.models import load_model

labels = os.listdir('data')

# === CONFIG ===
serial_port = 'COM5'
baud_rate = 115200
lines_per_packet = 500 * 1.5  # 500Hz for 2 second

# === SETUP ===
model = load_model("digit_classifier_model.h5")


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
            new_data = np.array([list(map(float, line.split(","))) for line in buffer])
            new_data = new_data.reshape(1, 750, 6)

            prediction = model.predict(new_data)
            predicted_class = np.argmax(prediction)
            print("Predicted digit:", predicted_class, "with confidence", prediction[0][predicted_class])

except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    ser.close()
