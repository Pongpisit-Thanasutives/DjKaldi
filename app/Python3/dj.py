#!/Users/pongpisit/anaconda3/bin/python
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
import connectViaSocket as client

interrupted = False

def reduce_noise():
    subprocess.call("./clean.sh")
    # replace pwd with your password
    pwd = ''
    proc = Popen(["sudo", "-S", "ffmpeg", "-i", "microphone-results-clean.wav", "-af", "highpass=300, lowpass=3400", "microphone-results-clean.wav"], stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True)
    proc.stdin.write("{}\n".format(pwd))
    out,err = proc.communicate(input="{}\n".format("y"))

def talk(sentence):
    engine.say(sentence)
    engine.runAndWait()

def state2event():
    # If you using 2018 acoustic model, you may want to apply this mapping before the return statement
    # mapping = {'สุ่ม' : 'ป๊อป', 'ป๊อป' : 'สุ่ม', 'อีดีเอ็ม' : 'อีดีเอ็ม', '':''}

    Microphone.record("state2-microphone-results.wav", 2.2)
    subprocess.call("./state2_clean.sh")

    # replace pwd with your password
    pwd = ''
    proc = Popen(["sudo", "-S", "ffmpeg", "-i", "state2-microphone-results-clean.wav", "-af", "highpass=300, lowpass=3400", "state2-microphone-results-clean.wav"], stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True)
    proc.stdin.write("{}\n".format(pwd))
    out,err = proc.communicate(input="{}\n".format("y"))
    
    count_penelties = 0
    while True:
        state2_command = subprocess.check_output(["/usr/local/opt/python/bin/python2.7", "/Users/pongpisit/Desktop/snowboy/app/Python3/state2_client.py", "-u", "ws://localhost:9000/client/ws/speech", "-r", "32000", "/Users/pongpisit/Desktop/snowboy/app/Python3/state2-microphone-results.wav"])
        if state2_command != '':
            state2_command = state2_command.decode('utf-8').replace('\n', '').split('.')[0].strip()
            # state2_command = mapping[state2_command]
            break
        else:
            count_penelties += 1
        if count_penelties == 2:
            state2_command = 'สุ่ม'
            break
    return state2_command

def detectedCallback():
    global detector, path, songs, numSongs, isEnd, state, now, player, kor, back, stop, engine, history, genre
    detector.terminate()

    # Response
    talk('Me kaldi')
    client.on_send_msg('มาละ')
    
    if state != 2: player.pause()
    Microphone.record("microphone-results.wav", 2.2)

    # Start recognition here
    command = ''
    count_penelties = 0
    reduce_noise()
    while True:
        result = subprocess.check_output(["/usr/local/opt/python/bin/python2.7", "/Users/pongpisit/Desktop/snowboy/app/Python3/newClient.py", "-u", "ws://localhost:8080/client/ws/speech", "-r", "32000", "/Users/pongpisit/Desktop/snowboy/app/Python3/microphone-results-clean.wav"])
        if result: 
            trans = result.decode('utf-8').replace('\n', '').split('.')[0]
            if trans != '':
                command = trans
                break
            else:
                count_penelties += 1
                if count_penelties == 2:break

    if command != '':
        if command == kor:
            print("Perform task: " + command)
            if state == 0:
                genre = state2event()
                print(genre)
                if genre == 'สุ่ม':
                    song = path + '/' + songs[randint(0, numSongs - 1)]
                elif genre == 'ป๊อป':
                    song = path + '/pop/' + popSongs[randint(0, numPopSongs - 1)]
                elif genre == 'อีดีเอ็ม':
                    song = path + '/edm/' + edmSongs[randint(0, numPopSongs - 1)]
                player = vlc.MediaPlayer(song)
                player.play()
                now += 1
                history.append(song)
                state = 1
                client.on_send_msg('กำลังเล่นเพลง,' + history[now].split('/')[-1] + ',' + path + ',' + genre + ',' + 'มั่นใจ')

            elif state == 1:
                genre = state2event()
                print(genre)
                player.stop()

                if genre == 'สุ่ม':
                    song = path + '/' + songs[randint(0, numSongs - 1)]
                elif genre == 'ป๊อป':
                    song = path + '/pop/' + popSongs[randint(0, numPopSongs - 1)]
                elif genre == 'อีดีเอ็ม':
                    song = path + '/edm/' + edmSongs[randint(0, numPopSongs - 1)]
                
                history.append(song)
                now += 1
                player = vlc.MediaPlayer(song)
                player.play()
                client.on_send_msg('กำลังเล่นเพลง,' + history[now].split('/')[-1] + ',' + path + ',' + genre + ',' + 'มั่นใจ')

            elif state == 2:
                if now > -1:
                    if history[now].split('/')[-2] == 'edm':
                        genre = 'อีดีเอ็ม'
                    elif history[now].split('/')[-2] == 'pop':
                        genre = 'ป๊อป'
                    player.play()
                    client.on_send_msg('กำลังเล่นเพลง,' + history[now].split('/')[-1] + ',' + path + ',' + history[now].split('/')[-2] + ',' + 'มั่นใจ')
                else:
                    client.on_send_msg('กำลังเล่นเพลง,' + '' + ',' + path + ',' + '' + ',' + 'มั่นใจ')
                state = 1

        elif command == stop:
            print("Perform task: " + command)
            print("Pause the song")
            if now > -1:
                client.on_send_msg('หยุดเล่นเพลง,' + history[now].split('/')[-1] + ',' + path)
                state = 2
            else:
                client.on_send_msg('หยุดเล่นเพลง,' + '' + ',' + path)
                state = 0

        elif command == back:
            if now != -1 and now != 0:
                print("Perform task: " + command)
                print("Back to the previous song")
                player.stop()
                player = vlc.MediaPlayer(history[now - 1])
                history = history[:now]
                now -= 1
                state = 1
                player.play()
                if history[now].split('/')[-1] == 'edm':
                    genre = 'อีดีเอ็ม'
                elif history[now].split('/')[-1] == 'pop':
                    genre = 'ป๊อป'
                client.on_send_msg('กำลังเล่นเพลง,' + history[now].split('/')[-1] + ',' + path + ',' + genre + ',' + 'มั่นใจ')
            else:
                print("Perform task: " + "หยุด เล่น")
                print("There is no previous song")
                print("Pause the song")
                client.on_send_msg('หยุดเล่นเพลง,' + '' + ',' + path)
                if now == 0:state = 2
                else:state = 0
        else:
            print("Not recognized as 1 of the commands or not sure, Please try again")
            if state == 1:
                player.play()
                client.on_send_msg('กำลังเล่นเพลง,' + history[now].split('/')[-1] + ',' + path + ',' + genre + ',' + 'ไม่มั่นใจ')
    else:        
        print("Please try again")
        if state == 1: 
            player.play()
            client.on_send_msg('กำลังเล่นเพลง,' + history[now].split('/')[-1] + ',' + path + ',' + genre + ',' + 'ไม่มั่นใจ')

    detector.start(detected_callback=detectedCallback,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

# Specify your model 'jarvis.umdl'
global model
model = 'dj_kaldi.pmdl'

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

global detector, path, songs, numSongs, isEnd, state, now, player, kor, back, stop, engine, history, genre
genre = ''
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.55)

# Set up
path = "/Users/pongpisit/Desktop/songs"
songs = [s for s in os.listdir(path) if '.mp3' in s]
numSongs = len(songs)
edmSongs = [s for s in os.listdir(path + '/edm') if '.mp3' in s]
numEdmSongs = len(edmSongs)
popSongs = [s for s in os.listdir(path + '/pop') if '.mp3' in s]
numPopSongs = len(popSongs)
isEnd = False
state = 0 # 0 = ไม่มีเพลงเล่น, 1 = มีเพลงเล่น, 2 = มีเพลงเล่นแต่หยุด

# Random the first song to play
history = [];
now = -1
song = ''
player = vlc.MediaPlayer()

kor = "ขอ เพลง "
stop = "หยุด เล่น "
back = "กลับ "

# main loop
engine = pyttsx3.init()
print("Start listening mode. . .")
client.on_send_msg('ว่าง')
detector.start(detected_callback=detectedCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)
detector.terminate()