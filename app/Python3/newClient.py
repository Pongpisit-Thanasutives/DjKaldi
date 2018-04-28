__author__ = 'tanel'

import argparse
from ws4py.client.threadedclient import WebSocketClient
import time
import threading
import sys
import urllib
import Queue
import json
import time
import os
from math import exp

def rate_limited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rate_limited_function(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rate_limited_function
    return decorate


class MyClient(WebSocketClient):

    def __init__(self, audiofile, url, protocols=None, extensions=None, heartbeat_freq=None, byterate=32000,
                 save_adaptation_state_filename=None, send_adaptation_state_filename=None):
        super(MyClient, self).__init__(url, protocols, extensions, heartbeat_freq)
        self.final_hyps = []
        self.audiofile = audiofile
        self.byterate = byterate
        self.final_hyp_queue = Queue.Queue()
        self.save_adaptation_state_filename = save_adaptation_state_filename
        self.send_adaptation_state_filename = send_adaptation_state_filename

    @rate_limited(4)
    def send_data(self, data):
        self.send(data, binary=True)

    def opened(self):
        def send_data_to_ws():
            with self.audiofile as audiostream:
                for block in iter(lambda: audiostream.read(self.byterate/4), ""):
                    self.send_data(block)
            # print >> sys.stderr, "Audio sent, now sending EOS"
            self.send("EOS")
        t = threading.Thread(target=send_data_to_ws)
        t.start()

    def received_message(self, m):
        response = json.loads(str(m))
        if response['status'] == 0:
            if 'result' in response:
                trans = response['result']['hypotheses'][0]['transcript']
                if response['result']['final']:
                    if len(response["result"]["hypotheses"]) > 1:
                        likelihood1 = response["result"]["hypotheses"][0]["likelihood"]
                        likelihood2 = response["result"]["hypotheses"][1]["likelihood"]
                        confidence = likelihood1 - likelihood2
                        confidence = 1 - exp(-confidence)
                    else:
                        confidence = 1.0e+10;
                    if confidence * 100 > 40:
                        self.final_hyps.append(trans)
                    else:
                        self.final_hyps.append('')
                        
    def get_full_hyp(self, timeout=120):
        return self.final_hyp_queue.get(timeout)

    def closed(self, code, reason=None):
        self.final_hyp_queue.put(" ".join(self.final_hyps))

def main():
    parser = argparse.ArgumentParser(description='Command line client for kaldigstserver')
    parser.add_argument('-u', '--uri', default="ws://localhost:8888/client/ws/speech", dest="uri", help="Server websocket URI")
    parser.add_argument('-r', '--rate', default=32000, dest="rate", type=int, help="Rate in bytes/sec at which audio should be sent to the server. NB! For raw 16-bit audio it must be 2*samplerate!")
    parser.add_argument('--save-adaptation-state', help="Save adaptation state to file")
    parser.add_argument('--send-adaptation-state', help="Send adaptation state from file")
    parser.add_argument('--content-type', default='', help="Use the specified content type (empty by default, for raw files the default is  audio/x-raw, layout=(string)interleaved, rate=(int)<rate>, format=(string)S16LE, channels=(int)1")
    parser.add_argument('audiofile', help="Audio file to be sent to the server", type=argparse.FileType('rb'), default=sys.stdin)
    args = parser.parse_args()

    content_type = args.content_type
    if content_type == '' and args.audiofile.name.endswith(".raw"):
        content_type = "audio/x-raw, layout=(string)interleaved, rate=(int)%d, format=(string)S16LE, channels=(int)1" %(args.rate/2)

    ws = MyClient(args.audiofile, args.uri + '?%s' % (urllib.urlencode([("content-type", content_type)])), byterate=args.rate,
                  save_adaptation_state_filename=args.save_adaptation_state, send_adaptation_state_filename=args.send_adaptation_state)
    ws.connect()
    result = ws.get_full_hyp()
    print result.encode('utf-8')

# python client.py -u ws://localhost:8080/client/ws/speech -r 32000 <testfile>.wav
if __name__ == "__main__":
    main()