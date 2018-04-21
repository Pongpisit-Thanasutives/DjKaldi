function [distance, dp] = d(template, test, x, y, mem)
	dp = mem
	if (x == 1 && y == 1)
		distance = sqrt(sum((template(:, 1) - test(:, 1)).^2));
		return;
	endif

	if (x < 1 || x > size(template)(2) || y < 1 || y > size(test)(2))
		distance = realmax;
		return;
	endif

	distance = realmax;
	e = sqrt(sum((template(:, x) - test(:, y)).^2));
	
	if (x-2 >= 1 && y-1 >= 1)
		if 	dp(size(test)(2)-(y-1)+1, x-2) != 0
			distance = min(distance, dp(size(test)-(y-1)+1, x-2) + 2 * e);
		else
			dp(size(test)(2)-(y-1)+1, x-2) = d(template, test, x-2, y-1, dp)(1)
			distance = min(distance, dp(size(test)(2)-(y-1)+1, x-2)+ 2 * e);
		endif
	endif

	if (x-1 >= 1 && y-1 >= 1)
		if dp(size(test)(2)-(y-1)+1, x-1) != 0
			distance = min(distance, dp(size(test)(2)-(y-1)+1, x-1) + e);
		else
			dp(size(test)(2)-(y-1)+1, x-1) = d(template, test, x-1, y-1, dp)(1)
			distance = min(distance, dp(size(test)(2)-(y-1)+1, x-1) + e);
		endif
	endif

	if (x-1 >= 1 && y-2 >= 1)
		if dp(size(test)(2)-(y-2)+1, x-1) != 0
			distance = min(distance, dp(size(test)(2)-(y-2)+1, x-1) + e);
		else
			dp(size(test)(2)-(y-2)+1, x-1) = d(template, test, x-1, y-2, dp)(1)
			distance = min(distance, mem(size(test)(2)-(y-2)+1, x-1) + e);
		endif
	endif
endfunction