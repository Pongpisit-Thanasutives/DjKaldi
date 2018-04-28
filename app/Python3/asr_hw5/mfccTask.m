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

%function[filtered] = highpass(y, original_with_no_dcoffset)
	%filtered = y - (0.97*reshape(original_with_no_dcoffset(160*49:160*49+400-1),1,400));
%endfunction

function[filtered] = highpass(y, original_with_no_dcoffset, n)
	past = n-1
	if past!=0
		filtered = y - (0.97*reshape(original_with_no_dcoffset(160*past:160*past+400-1),1,400));
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

gas_station_sound = wavread('gas_station.wav');
length_ms = (size(gas_station_sound)(1) / 16000);
average = mean(gas_station_sound);
gas_station_sound -= average
frames = toFrames(gas_station_sound, 16000);

frame_50 = frames(50, :)

LogE_frame_50 = getLogE(frame_50)
%plot(abs(fft(frame_50)))

highpass_frame_50 = highpass(frame_50, gas_station_sound, 50)
%plot(abs(fft(highpass_frame_50)))

spectrum_frame_50 = abs(hammingAndFft(highpass_frame_50));
%plot(spectrum_frame_50);
%xlabel('frequency (Hz)');

load('mel_filters.mat')

spectrum_frame_50 = spectrum_frame_50(1:257);
%plot(spectrum_frame_50);
%xlabel('frequency (Hz)');

MFSCs = max(-50, log(spectrum_frame_50 * mel_filters))
MFCC = getMFCC(transpose(MFSCs))
MFCC_features = [LogE_frame_50;MFCC];

load('gas_station_mfcc.mat');
test = transpose(transpose(gas_station_mfcc)(50,:))
distance = 0
for k = 1:14
	distance += (MFCC_features(k, 1)- test(k, 1)) ** 2;
endfor