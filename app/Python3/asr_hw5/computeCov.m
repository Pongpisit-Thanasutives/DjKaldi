load('gas_station_mfcc.mat');

logE = gas_station_mfcc(1, :);
max_cov = -1;
max_index = -1;

for i = 2:14
	if cov(logE, gas_station_mfcc(i, :)) > max_cov
		max_index = i
		max_cov = max(max_cov, cov(logE, gas_station_mfcc(i, :)));
	endif
endfor