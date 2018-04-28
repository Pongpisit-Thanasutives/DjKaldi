def mcs(mymem, string1, string2, i,j):
	if i==0:
		if string1[i] in string2[0:j+1]:
			return 1
		else:
			return 0 
	elif j==0:
		if string2[j] in string1[0:i+1]:
			return 1
		else:
			return 0
	else:
		if string1[i]==string2[j]:
			if (i-1,j-1) in mymem:
				return mymem[(i-1,j-1)]+1
			else:
				mymem[(i-1,j-1)] = mcs(mymem, string1, string2, i-1,j-1) 
				return mymem[(i-1,j-1)]+1
		else:
			if (i-1,j) in mymem:
				left = mymem[(i-1,j)]
			else:
				left = mcs(mymem, string1, string2, i-1,j)
				mymem[(i-1,j)] = left
			if (i,j-1) in mymem:
				right = mymem[(i,j-1)]
			else:
				right = mcs(mymem, string1, string2, i,j-1)
				mymem[(i,j-1)] = right
			return max(left,right)
# print(mcs({}, x, y, len(x)-1, len(y)-1))