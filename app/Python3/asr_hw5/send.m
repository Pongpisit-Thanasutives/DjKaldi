clear;
function[frames] = toFrames(y,fs)
	y = transpose(y);
 	index = 1;
	fWidth = floor(25 / 1000 * fs)
	shift = floor(10 / 1000 * fs)
	frameAmount = 1 + ceil((length(y) - fWidth) / shift);
	leftOff = shift * (frameAmount - 1) - (length(y) - fWidth)
	y = [y, zeros(1,leftOff)];
	frames = zeros(frameAmount,fWidth);
	for i = 1:frameAmount
		frames(i,:) = y(1,index:(index+fWidth-1));
    	index += shift;
  	endfor
endfunction

function[LogE] = getLogE(frame)
	sum = 0;
	for i = 1:length(frame)
		sum += frame(i) ** 2;
	endfor
	LogE = max(-50,log(sum));
endfunction

function[filtered] = highpass(y, original_with_no_dcoffset, n)
	past = n-1
	if past > 0
		stop = min(160*past+400-1, size(original_with_no_dcoffset)(1))
		tmp = 0.97*reshape(original_with_no_dcoffset(160*past:stop),1,abs(stop - 160*past + 1));
		if size(original_with_no_dcoffset)(2) < 160*past+400-1
			tmp = [tmp zeros(1, 400 - size(tmp)(2))]
		endif
		filtered = y - tmp;
	else
		filtered = y	
	endif
endfunction

function[result] = hammingAndFft(frame)
	frame = frame.*transpose(hamming(length(frame)));
	frame = [frame, zeros(1,512 - length(frame))];
	result = fft(frame);
endfunction

function[result] = getMFCC(MFSCs)
	result = zeros(13, 1);
	for s = 0:12
		sum = 0;
		for j = 1:23
			sum += 	MFSCs(j, 1) * cos((j - 0.5) * pi * s / 23);
		endfor
		result(s+1, 1) = sum;
	endfor
endfunction

function[result] = compute_mfcc(filename)

	gas_station_sound = wavread(filename);
	length_ms = (size(gas_station_sound)(1) / 16000);
	average = mean(gas_station_sound);
	gas_station_sound -= average
	
	frames = toFrames(gas_station_sound, 16000);

	load('mel_filters.mat')

	result = zeros(size(frames)(1), 14)
	for f = 1:144
		frame_capture = frames(f, :)

		LogE_frame_capture = getLogE(frame_capture)

		highpass_frame_capture = highpass(frame_capture, gas_station_sound, f)

		spectrum_frame_capture = abs(hammingAndFft(highpass_frame_capture));

		spectrum_frame_capture = spectrum_frame_capture(1:257);
		MFSCs = max(-50, log(spectrum_frame_capture * mel_filters))
		MFCC = getMFCC(transpose(MFSCs))
		MFCC_features = [LogE_frame_capture;MFCC];

		result(f,:) =  MFCC_features
	endfor
	
	result = transpose(result)
	for i= 1:size(result)(1)
		result(i, :) -= mean(result(i, :))
	endfor
endfunction