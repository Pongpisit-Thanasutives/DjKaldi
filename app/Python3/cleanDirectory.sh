#!/bin/bash
path=$1
for fullfilename in ${path}*; do
	filename=$(basename "$fullfilename")
	ext="${filename##*.}"
	if [ "$ext" != ".mp3" ]; then 
		fileWithNoExtension="${filename%%.*}"
		outputfile="${path}${fileWithNoExtension}.mp3"
		ffmpeg -i $fullfilename $outputfile
	fi
done;