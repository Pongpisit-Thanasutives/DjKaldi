# ASR
Chulalongkorn university automatic speech recognition homeworks

For server
docker pull jcsilva/docker-kaldi-gstreamer-server
and put models under opt/

To start the first model /opt/start.sh -y /opt/models/newmodel/sample_nnet2.yaml at /

To start the second model /opt/start.sh -y /opt/models/newmodel2/sample_nnet2.yaml at /

For client
The first model: python2 client.py -u ws://localhost:8080/client/ws/speech -r 32000 <testfile>.wav
The second model: python2 client.py -u ws://localhost:9000/client/ws/speech -r 32000 <testfile>.wav
