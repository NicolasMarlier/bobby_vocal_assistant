import sounddevice as sd
import struct
import numpy as np

play_recording = []

with open("recordings/orders/1516229665730.dat", "r") as file:
    data = file.read()

for i in range(0, len(data) / 8):
  play_recording.append(np.array(struct.unpack('2f', data[i*8:(i+1)*8])).astype("f"))

samplerate = 44100.0
stream = sd.play(play_recording, samplerate, blocking=True)