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

function[result] = melFilter(spectrum,mel)
	mel = transpose(mel);
	mel_length = size(mel,2);
	result = zeros(size(mel,1),size(mel,2));
	for i = 1:size(mel,1)
		result(i,:) = spectrum .* mel(i,:);
	endfor
endfunction

function[result] = getEnergy(filtered_spectrum,mel)
	t_mel = transpose(mel);
	result = zeros(23, 1);
	for i = 1:23
		result(i, 1) = sum(filtered_spectrum(i,:))
	endfor
endfunction

function[result] = getMFSCs(filtered_spectrum,mel)
	result = max(-50 ,log(getEnergy(filtered_spectrum, mel)))
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

gas_station_sound = audioread('gas_station.wav');
length_ms = (size(gas_station_sound)(1) / 16000);
average = mean(gas_station_sound);
for(i = 1:length(gas_station_sound))
	gas_station_sound(i) = gas_station_sound(i) - average;
end;
frames = toFrames(gas_station_sound, 16000);

max_distance = 0
load('mel_filters.mat')
load('gas_station_mfcc.mat');
dis = zeros(144, 1)
for f = 1:144
	frame_capture = frames(f, :)

	LogE_frame_capture = getLogE(frame_capture)
	%plot(abs(fft(frame_capture)))

	highpass_frame_capture = highpass(frame_capture, gas_station_sound, f)
	%plot(abs(fft(highpass_frame_capture)))

	spectrum_frame_capture = abs(hammingAndFft(highpass_frame_capture));
	%plot(spectrum_frame_capture);
	%xlabel('frequency (Hz)');

	spectrum_frame_capture = spectrum_frame_capture(1:257);
	mft = melFilter (spectrum_frame_capture, mel_filters);
	MFSCs = getMFSCs(mft, mel_filters)
	MFCC = getMFCC(MFSCs)
	MFCC_features = [LogE_frame_capture;MFCC];

	test = transpose(transpose(gas_station_mfcc)(f,:))
	distance = 0
	for k = 1:14
		distance += (MFCC_features(k, 1)- test(k, 1)) ** 2;
	endfor

	max_distance = max(max_distance, distance)
	dis(f, 1) = distance
endfor
dis = sort(dis)