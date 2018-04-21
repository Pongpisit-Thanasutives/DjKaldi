import pyaudio
import wave 
from pysine import sine

def record():
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 16000
	CHUNK = 16384
	RECORD_SECONDS = 2.7
	WAVE_OUTPUT_FILENAME = "microphone-results.wav"
	audio = pyaudio.PyAudio()
	
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
	                rate=RATE, input=True,
	                frames_per_buffer=CHUNK)

	# Signal telling the user to speak
	sine(frequency=250.0, duration=0.25)

	print("recording...")
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	print("finished recording")
	 
	 
	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	 
	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

# record()