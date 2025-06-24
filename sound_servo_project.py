import numpy as np
import sounddevice as sd
import tensorflow as tf
import serial
import time
import cv2

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="soundclassifier_with_metadata.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

SERIAL_PORT = 'COM7'  # Change based on your system
BAUD_RATE = 9600
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

# Model expects ~1 second of audio input
SAMPLING_RATE = 16000
DURATION = 2.752  # seconds

labels = ['Background Noise','Close','Open']  # Teachable Machine class order

def classify_audio():
    print("Recording...")
    audio = sd.rec(int(SAMPLING_RATE * DURATION), samplerate=SAMPLING_RATE, channels=1, dtype='float32')
    sd.wait()

    audio = np.squeeze(audio)            # shape: (16000,)
    audio = np.expand_dims(audio, axis=0)  # shape: (1, 16000)

    interpreter.set_tensor(input_details[0]['index'], audio)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]

    top_idx = np.argmax(output_data)
    confidence = output_data[top_idx]
    prediction = labels[top_idx]
    print(f"Detected: {prediction} ({confidence:.2f})")

    if confidence > 0.50:  # threshold
        if prediction == 'Open':
            ser.write(b'o')
        elif prediction == 'Close':
            ser.write(b'c')
        else:
            ser.write(b'b')  # not required, but safe fallback


    

try:
    while True:
        classify_audio()
        time.sleep(0.5)  # adjust for smooth operation
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
