# About
Chulalongkorn university automatic speech recognition term project

# To start ASR server
docker pull jcsilva/docker-kaldi-gstreamer-server
and put models folder under opt/

---

To start the first model(1st stage) using the 2018 acoustic model (bugs) `/opt/start.sh -y /opt/models/newmodel/sample_nnet2.yaml` at / of the docker

To start the first model(1st stage) using the 2017 acoustic model (working) `/opt/start.sh -y /opt/models/model/sample_nnet2.yaml` at / of the docker

To start the second model(2nd stage) using the 2018 acoustic model (bugs) `/opt/start.sh -y /opt/models/newmodel2/sample_nnet2.yaml` at / of the docker

To start the second model(2nd stage) using the 2017 acoustic model (woking) `/opt/start.sh -y /opt/models/model2/sample_nnet2.yaml` at / of the docker

# For client
The first model: `python2 client.py -u ws://localhost:8080/client/ws/speech -r 32000 testfile.wav`

The second model: `python2 client.py -u ws://localhost:9000/client/ws/speech -r 32000 testfile.wav`

# To install the dependencies
1. `pip3 install python-vlc`  
2. `pip3 install pyttsx3`  
3. `pip3 install pyaudio`  
4. `pip3 install pysine`  
5. `brew install sox`  
6. `brew install ffmpeg`

# To run the bot
1. At least you need to start the backend server. Clone https://github.com/kamemos/ASR-Project and npm start at /asr-back 

2. Run `python dj.py` or `./dj.sh` from wherever in your computer (Make sure that the directories inside the bash script are correct.)