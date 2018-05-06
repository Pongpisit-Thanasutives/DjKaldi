#!/bin/sh
sox state2-microphone-results.wav state2-noise-audio.wav trim 0 0.47
sox state2-noise-audio.wav -n noiseprof state2-noise.prof
sox state2-microphone-results.wav state2-microphone-results-clean.wav noisered noise.prof 0.25