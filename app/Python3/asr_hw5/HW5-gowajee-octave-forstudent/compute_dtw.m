function [result] = compute_dtw(template,test)
    result = realmax;
    mem = zeros(size(test)(2), size(template)(2));
    c = 0;
    printf('c %d\n',c);
    for y = size(template)(2) - 50:(template)(2) + 50
    	printf('c %d\n',c);
    	result = min(result, d(template, test, size(template)(2), y, mem)(1));
    	mem = d(template, test, size(template)(2), y, mem)(2);
    endfor
endfunction