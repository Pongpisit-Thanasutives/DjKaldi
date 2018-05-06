# ASR
Chulalongkorn university automatic speech recognition homeworks

For server
docker pull jcsilva/docker-kaldi-gstreamer-server
and put models under opt/

Lastly, /opt/start.sh -y /opt/models/newmodel/sample_nnet2.yaml at /

For client
python2 client.py -u ws://localhost:8080/client/ws/speech -r 32000 <testfile>.wav
