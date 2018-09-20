import sounddevice as sd
import sys
import scipy

maxi = 0
max_amp = 1
current_max = 0
signal = []

def audio_callback(indata, frames, time, status):
  global current_max
  global signal
  signal = [max([abs(d) for d in data]) for data in indata]
  foft = abs(scipy.fft(signal))
  #maxi = min([max_amp, max([max([abs(d) for d in data]) for data in indata])])
  max_foft = max(foft)
  sys.stdout.write("\r" + "".join(["|" if val > max_foft / 10 else " " for val in foft[0:100]]))
  #current_max = max([current_max * 0.9, maxi])
  #nb_of_bars = int(round(current_max * 99 / max_amp)) + 1
  #sys.stdout.write("\r" + ("|" * nb_of_bars) + (" " * (100 - nb_of_bars)))
  sys.stdout.flush()


try:
  stream = sd.InputStream(device=0, channels=2, samplerate=44100.0, callback=audio_callback)
  with stream:
    while True:
      a=0#print("ok")
except KeyboardInterrupt:
    print('Interrupted by user')
