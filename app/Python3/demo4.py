import snowboydecoder
import sys
import signal
import speech_recognition as sr
import os
import subprocess
from statistics import mode, StatisticsError

"""
This demo file shows you how to use the new_message_callback to interact with
the recorded audio after a keyword is spoken. It uses the speech recognition
library in order to convert the recorded audio into text.

Information on installing the speech recognition library can be found at:
https://pypi.python.org/pypi/SpeechRecognition/
"""


interrupted = False


def audioRecorderCallback(fname):
    print("converting audio to text")
    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:
        audio = r.record(source)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    # try:
    #     # for testing purposes, we're just using the default API key
    #     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    #     # instead of `r.recognize_google(audio)`
    #     print(r.recognize_google(audio, language='th-TH'))
    
    try:
        with open("microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())
        
        # Find what the command was ?
        command = ''
        all_result = ['', '', '']
        for i in range(3):
            while True:
                result = subprocess.check_output(["/usr/local/opt/python/bin/python2.7", "client.py", "-u", "ws://localhost:8080/client/ws/speech", "-r", "32000", "microphone-results.wav"])
                if result: 
                    trans = result.decode('utf-8').replace('\n', '')
                    if len(trans) != 0: break
            print(i, trans)
            all_result[i] = trans
            print(all_result)
            if i != 0:
                try:
                    if mode(all_result) != '':
                        command = mode(all_result).split('.')[0]
                except StatisticsError:
                    if i == 2: pass
                    else: command = all_result[2].split('.')[0]
                break

        if command != '':
            print(command)
        else:
            print("Please try again")

    except sr.RequestError as e:
        print("Could not understand audio, continue playing. . .")
        player.play()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    os.remove(fname)

def detectedCallback():
  print('recording audio...', end='', flush=True)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.38)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detectedCallback,
               audio_recorder_callback=audioRecorderCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.01)
detector.terminate()