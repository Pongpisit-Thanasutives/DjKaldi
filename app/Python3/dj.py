import snowboydecoder
import sys
import signal
import Microphone
import subprocess
import getpass
from subprocess import Popen, PIPE
import os
import vlc
import pyttsx3
from random import randint
import speech_recognition as sr

interrupted = False

def reduce_noise():
    pwd = getpass.getpass()
    proc = Popen(["sudo", "-S", "ffmpeg", "-i", "microphone-results.wav", "-af", "highpass=f=300, lowpass=f=8000", "microphone-results.wav"], stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True)
    proc.stdin.write("{}\n".format(pwd))
    out,err = proc.communicate(input="{}\n".format("y"))

def talk(sentence):
    engine.say(sentence)
    engine.runAndWait()

def detectedCallback():
    global detector, path, songs, numSongs, isEnd, state, now, player, kor, back, stop, engine, history
    detector.terminate()

    # Response
    talk('Me kaldi')
    
    if state != 2: player.pause()
    snowboydecoder.play_audio_file
    Microphone.record()

    # Start recognition here
    command = ''
    count_penelties = 0
    while True:
        reduce_noise()
        result = subprocess.check_output(["/usr/local/opt/python/bin/python2.7", "/Users/pongpisit/Desktop/snowboy/app/Python3/newClient.py", "-u", "ws://localhost:8080/client/ws/speech", "-r", "32000", "/Users/pongpisit/Desktop/snowboy/app/Python3/microphone-results.wav"])
        if result: 
            trans = result.decode('utf-8').replace('\n', '').split('.')[0]
            if trans != '':
                command = trans
                break
            else:
                count_penelties += 1
                # print(count_penelties)
                if count_penelties == 2:break
    # print(count_penelties)

    if command != '':
        if command == kor:
            print("Perform task: " + command)
            if state == 0:
                talk(songs[now])
                player.play()
                state = 1

            elif state == 1:
                player.stop()
                next_rnd = randint(0, numSongs - 1)
                while(next_rnd == history[now]):
                    next_rnd = randint(0, numSongs - 1)
                history.append(next_rnd)
                now += 1

                song = path + '/' + songs[history[now]]
                player = vlc.MediaPlayer(song)
                talk(songs[now])
                player.play()

            elif state == 2:
                talk(songs[now])
                player.play()
                state = 1

        elif command == stop:
            print("Perform task: " + command)
            print("pause the song")
            state = 2

        elif command == back:
            if now != 0:
                print("Perform task: " + command)
                print("back to the previous song")
                player.stop()
                player = vlc.MediaPlayer(path + '/' + songs[history[now - 1]])
                history = history[:now]
                now -= 1
                state = 1
                talk(songs[now])
                player.play()
            else:
                print("Perform task: " + "หยุด เล่น")
                print("There is no previous song")
                print("pause the song")
                state = 2
        else:
            print("Not recognized as 1 of the commands or not sure, Please try again")
            if state == 1:
                talk(songs[now])
                player.play()
    else:
        # print("Please try again")
        # talk('Mai roo jak')
        
        ### Uncomment this to get only kaldi engine ###
        # print("Please try again")
        # if state == 1: player.play()

        # use the audio file as the audio source
        r = sr.Recognizer()
        with sr.AudioFile("microphone-results.wav") as source:
            audio = r.record(source)  # read the entire audio file

        # recognize speech using recognize_google
        try:
            command = r.recognize_google(audio, language="th-TH")

            if command != '':
                if command == "ขอเพลง":
                    print("Perform task: " + kor)
                    if state == 0:
                        player.play()
                        state = 1

                    elif state == 1:
                        player.stop()
                        next_rnd = randint(0, numSongs - 1)
                        while(next_rnd == history[now]):
                            next_rnd = randint(0, numSongs - 1)
                        history.append(next_rnd)
                        now += 1

                        song = path + '/' + songs[history[now]]
                        player = vlc.MediaPlayer(song)
                        player.play()

                    elif state == 2:
                        player.play()
                        state = 1

                elif command == "หยุดเล่น":
                    print("Perform task: " + stop)
                    print("pause the song")
                    state = 2

                elif command == "กลับ":
                    if now != 0:
                        print("Perform task: " + command)
                        print("back to the previous song")
                        player.stop()
                        player = vlc.MediaPlayer(path + '/' + songs[history[now - 1]])
                        history = history[:now]
                        now -= 1
                        state = 1
                        player.play()
                    else:
                        print("Perform task: " + "หยุด เล่น")
                        print("There is no previous song")
                        print("pause the song")
                        state = 2
                else:
                    print("Not recognized as 1 of the commands or not sure, Please try again")
                    if state == 1: player.play()
            else:
                print("Please try again")
                if state == 1: player.play()    
        except:
            print("Please try again")
            if state == 1: player.play()

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.6)
    detector.start(detected_callback=detectedCallback,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

### Main starts here ###
# if len(sys.argv) != 2:
#     print("Error: need to specify model name and the directory containing")
#     sys.exit(-1)

# Specify your model
global model
model = 'dj_kaldi.pmdl'

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

global detector, path, songs, numSongs, isEnd, state, now, player, kor, back, stop, engine, history
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

# Set up
path = "/Users/pongpisit/Desktop/songs"
songs = os.listdir(path)
numSongs = len(songs)
isEnd = False
state = 0 # 0 = ไม่มีเพลงเล่น, 1 = มีเพลงเล่น, 2 = มีเพลงเล่นแต่หยุด

# Random the first song to play
history = []; history.append(randint(0, numSongs - 1))
now = 0
song = path + '/' + songs[history[now]]

player = vlc.MediaPlayer(song)

kor = "ขอ เพลง "
stop = "หยุด เล่น "
back = "กลับ "

# main loop
engine = pyttsx3.init()
print("Start listening mode. . .")
detector.start(detected_callback=detectedCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)
detector.terminate()
