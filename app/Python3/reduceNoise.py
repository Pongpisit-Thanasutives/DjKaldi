import subprocess
import getpass
from subprocess import Popen, PIPE

# def reduce(inFile, outFile):
# 	# ffmpeg -i <input_file> -af "highpass=f=200, lowpass=f=3000" <output_file>
# 	res = subprocess.check_output(["ffmpeg", "-i", inFile, "-af", "highpass=f=300, lowpass=f=3400", outFile])
# 	return res
inFile = "microphone-results.wav"
outFile = "microphone-results.wav"

pwd = getpass.getpass()
proc = Popen(["sudo", "-S", "ffmpeg", "-i", "microphone-results.wav", "-af", "highpass=f=300, lowpass=f=3400", "microphone-results.wav"], stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True)
proc.stdin.write("{}\n".format(pwd))
out,err = proc.communicate(input="{}\n".format("y"))