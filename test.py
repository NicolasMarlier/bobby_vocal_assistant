import time
import sounddevice as sd

duration = 3
fs = 48000
print("Will record in a sec")
time.sleep(0.5)
print("Recording")
myrecording = sd.rec(duration * fs, channels=2, device=0, blocking=True)



print(myrecording[1000:2000])
print("Done recording, will play in a sec")
time.sleep(0.5)
sd.play(myrecording, samplerate=fs, blocking=True)

