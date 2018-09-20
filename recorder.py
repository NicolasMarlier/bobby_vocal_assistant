import sounddevice as sd
import sys
import os
from pynput import keyboard
import time
import pickle

import struct



def audio_callback(indata, frames, time, status):

  global recording
  global should_record
  if should_record != None:
    recording.extend([d.tolist() for d in indata])


def on_press(key):
    global should_record
    if key == keyboard.Key.cmd:    
        should_record = "order"
        prnt(u"\x1B[32m\u2022\x1B[0m")
    if key == keyboard.Key.ctrl:    
        should_record = "no_order"
        prnt(u"\x1B[31m\u2022\x1B[0m")

def on_release(key):
    sys.exit()

# Collect events until released

recording = []
should_record = None
def ready_to_record():
  global should_record
  global recording
  should_record = None
  prnt("")
  recording = []
  samplerate = 44100.0
  stream = sd.InputStream(device=0, channels=2, samplerate=samplerate, callback=audio_callback)  
  with stream:
    lis = keyboard.Listener(on_press=on_press, on_release=on_release)
    lis.start()
    while lis.isAlive():
      a=0

    prnt("...")

    data=""
    if(len(recording) > 15000):
      for record in recording:
          data += struct.pack('2f', *record)
      
      if should_record == 'order':
        filename = 'recordings/orders/%i.dat' % int(round(time.time()*1000))
      else:
        filename = 'recordings/no_orders/%i.dat' % int(round(time.time()*1000))
      with open(filename, 'w+') as f:
        f.write(data)


def record():
  
  os.system('clear')
  print("Press and hold to record: (Cmd: order | Ctrl: no order)\n\n")
  while 1==1:
    ready_to_record()

def prnt(str):
  print "\r%s%s" % (str, " " * 100),
  sys.stdout.flush()

record()
