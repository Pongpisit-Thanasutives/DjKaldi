import snowboydecoder
import sys
import signal
import Microphone
import subprocess


interrupted = False
p = subprocess.Popen(["open", "logo.png"])

def fun():
    print("GOT YOU!")

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

# if len(sys.argv) == 1:
#     print("Error: need to specify model name")
#     print("Usage: python demo.py your.model")
#     sys.exit(-1)

model = 'dj_kaldi.pmdl'

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

# main loop
detector.start(detected_callback=fun,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)
detector.terminate()
