from math import sqrt
from scipy.spatial.distance import euclidean

template = [[1,-1], [3,3], [8,7], [4,-5], [5,4]]
test = [[2,0], [2,4], [4,2], [4,-4], [6,3]]

mymap = {}
dp = {} 

for i in range(len(test)):
	for j in range(len(template)):
		mymap[(i + 1, j + 1)] = euclidean(test[i], template[j])

for j in range(len(template), 0, -1):
	s = ''
	for i in range(1, len(test) + 1):
		s += str(mymap[(i, j)]) + ' '
	print(s)
print()

def dtw(n, m):
	global mymap
	# if abs(n - m) >= 3: return float('inf')
	if n == 1 and m == 1: return mymap[(n, m)]
	
	mini = float('inf')
	if (n-2, m-1) in mymap:
		mini = min(mini, dtw(n-2, m-1) + 2 * mymap[(n, m)])
	if (n-1, m-1) in mymap:
		mini = min(mini, dtw(n-1, m-1) + mymap[(n, m)])
	if (n-1, m-2) in mymap:
		mini = min(mini, dtw(n-1, m-2) + mymap[(n, m)])

	return mini

for j in range(len(template), 0, -1):
	s = ''
	for i in range(1, len(test) + 1):
		s += str(dtw(i, j)) + '  '
	print(s)
print()

path = []
xEnd, yEnd = len(test), len(template)
path.append([(xEnd,yEnd,dtw(xEnd, yEnd))])

while(xEnd != 1 or yEnd != 1):
	ls = []
	k = dtw(xEnd, yEnd)
	tmpX = xEnd
	tmpY = yEnd

	if k == dtw(tmpX-2, tmpY-1) + 2 * mymap[(tmpX, tmpY)]:
		xEnd = tmpX - 2
		yEnd = tmpY - 1
		ls.append((xEnd, yEnd, dtw(tmpX-2, tmpY-1)))

	elif k == dtw(tmpX-1, tmpY-1) + mymap[(tmpX, tmpY)]:
		xEnd = tmpX - 1
		yEnd = tmpY - 1
		ls.append((xEnd, yEnd, dtw(tmpX-1, tmpY-1)))

	elif k == dtw(tmpX-1, tmpY-2) + mymap[(tmpX, tmpY)]:
		xEnd = tmpX - 1
		yEnd = tmpY - 2
		ls.append((xEnd, yEnd, dtw(tmpX-1, tmpY-2)))

	path.append(ls)
		
print(path)