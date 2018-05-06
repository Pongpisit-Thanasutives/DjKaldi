#!/bin/sh
sox microphone-results.wav noise-audio.wav trim 0 0.47
sox noise-audio.wav -n noiseprof noise.prof
sox microphone-results.wav microphone-results-clean.wav noisered noise.prof 0.25