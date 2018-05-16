# About the project
Chulalongkorn university automatic speech recognition term project

# To start ASR servers
1. `docker pull jcsilva/docker-kaldi-gstreamer-server` and **put models folder under opt/**
2. To start the 1st stage server: `docker run -it -p 8080:80 -v <path_to_model>:/opt/models jcsilva/docker-kaldi-gstreamer-server:latest /bin/bash`  
3. To start the 2nd stage server: `docker run -it -p 9000:80 -v <path_to_model>:/opt/models jcsilva/docker-kaldi-gstreamer-server:latest /bin/bash`
---
To start the first ASR engine(1st stage) using the 2018 acoustic model (bugs) `/opt/start.sh -y /opt/models/newmodel/sample_nnet2.yaml` at **/ of the docker (port = 8080)**  
To start the first ASR engine(1st stage) using the 2017 acoustic model (working) `/opt/start.sh -y /opt/models/model/sample_nnet2.yaml` **at / of the docker (port = 8080)**  
To start the second ASR engine(2nd stage) using the 2018 acoustic model (bugs) `/opt/start.sh -y /opt/models/newmodel2/sample_nnet2.yaml` **at / of the docker (port = 9000)**  
To start the second ASR engine(2nd stage) using the 2017 acoustic model (woking) `/opt/start.sh -y /opt/models/model2/sample_nnet2.yaml` **at / of the docker (port = 9000)**

# For client
The first model: `python2 client.py -u ws://localhost:8080/client/ws/speech -r 32000 testfile.wav`  
The second model: `python2 client.py -u ws://localhost:9000/client/ws/speech -r 32000 testfile.wav`

# To install the dependencies
1. `pip3 install python-vlc`  
2. `pip3 install pyttsx3` 
3. `brew install portaudio` 
4. `pip3 install pyaudio`  
5. `pip3 install pysine`  
6. `brew install sox`  
7. `brew install ffmpeg`

# To run the bot
1. At least you need to start the backend server. Clone https://github.com/kamemos/ASR-Project and npm start at /asr-back  
2. Run `python dj.py` or `./dj.sh` from wherever in your computer (Make sure that the directories inside the bash script are correct.)

# Important notes about the directory containing your songs and misc
1. (line 198) path is the string variable which tells the program where your songs locate. In the original code it is `"/Users/pongpisit/Desktop/songs"`  
2. path should contain random songs, 1 directory named edm which contains edm songs (e.g. `"/Users/pongpisit/Desktop/songs/edm"`) and 1 directory named pop which contains pop songs (e.g. `"/Users/pongpisit/Desktop/songs/pop"`)  
3. Change the code at line 44 and 72 in dj.py. They should be changed to `["/path/to/executable/python2.7", "/path/to/state2_client.py", "-u", "ws://localhost:9000/client/ws/speech", "-r", "32000", "/path/to/state2-microphone-results.wav"]` and `["/path/to/python2.7", "/path/to/newClient.py", "-u", "ws://localhost:8080/client/ws/speech", "-r", "32000", "/path/to/microphone-results-clean.wav"]` respectively.  
4. Replace pwd at line 37 in dj.py with your password.

# Demo
https://www.youtube.com/watch?v=VVPDA6bHqH8&feature=youtu.be