import glob
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

X = []
y = []
digits = 9

for digit in range(digits):
    folder = f'data/label_{digit}'
    files = glob.glob(folder + '/*.txt')
    
    for file in files:
        data = np.loadtxt(file, delimiter=',')
        X.append(data)
        y.append(digit)

X = np.array(X)
y = np.array(y)

print("Loaded", X.shape[0], "samples of shape", X.shape[1:])

model = Sequential([
    LSTM(64, input_shape=(750, 6)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dense(digits, activation='softmax')  # 10 classes for 0-9
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print("Training model...")
model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)

model.save("digit_classifier_model.h5")
print("Model saved as digit_classifier_model.h5")
