#!/bin/sh
sox microphone-results.wav -n noiseprof noise.prof
sox microphone-results.wav microphone-results-clean.wav noisered noise.prof 0.21