from scipy.io import loadmat
from scipy.spatial.distance import euclidean
import numpy as np
import matplotlib.pyplot as plt

mat = loadmat('data.mat')
template = mat['templates'][0][0]

mem = {}

def d(x, y, template, test):
	global mem
	if x==0 and y==0: 
		return euclidean(template[0], test[0])
	
	mini = float('inf')
	dis = euclidean(template[x], test[y])

	if x-2>=0 and y-1>=0:
		if (x-2, y-1) in mem:
			mini = min(mini, mem[(x-2, y-1)] + 2 * dis)
		else:
			mem[(x-2, y-1)] = d(x-2, y-1, template, test)
			mini = min(mini, mem[(x-2, y-1)] + 2 * dis)

	if x-1>=0 and y-1>=0:
		if (x-1, y-1) in mem:
			mini = min(mini, mem[(x-1, y-1)] + dis)
		else:
			mem[(x-1, y-1)] = d(x-1, y-1, template, test)
			mini = min(mini, mem[(x-1, y-1)] + dis)

	if x-1>=0 and y-2>=0:
		if (x-1, y-2) in mem:
			mini = min(mini, mem[(x-1, y-2)] + dis)
		else:
			mem[(x-1, y-2)] = d(x-1, y-1, template, test)
			mini = min(mini, mem[(x-1, y-2)] + dis)

	return mini

def dtw(template, test):
	minimum = float('inf')
	for y in range(len(template) - 51, len(template) + 50):
		minimum = min(minimum, d(len(template)-1, y, template, test))
	return minimum

def slidedtw(template, test):
	global mem
	dists = []
	testind = 0
	lentest = test.shape[1]
	lentemp = template.shape[1]
	globalcon = 50
	while testind + lentemp + globalcon < lentest:
		mem = {}
		dists.append(dtw(template.T,test[:, testind:testind+lentemp+globalcon+1].T))
		testind = testind + round(globalcon / 2)
	return dists

def computeall(temp, yeses, noes):
	yesd = np.zeros(len(yeses))
	for i in range(len(yeses)):
		yesd[i] = min(slidedtw(temp, yeses[i]))
	nod = []
	for i in range(len(noes)):
		nod.extend(slidedtw(temp, noes[i]))
	return (np.array(yesd), np.array(nod))

def computeRoc(yesscores, noscores):
	allscores = []
	allscores.extend(yesscores)
	allscores.extend(noscores)
	totalyes = len(yesscores)
	totalno = len(noscores)
	minsc = min(allscores)
	maxsc = max(allscores)
	thres = [x for x in np.arange(minsc, maxsc, (maxsc-minsc)/100)]
	FP = np.zeros(len(thres))
	TP = np.zeros(len(thres))	
	for i in range(len(thres)):
		TP[i] = sum(yesscores < thres[i]) / totalyes
		FP[i] = sum(noscores < thres[i]) / totalno
	return (FP, TP)

tmp1, tmp2 = computeall(template, mat['mfccs_yes'][0], mat['mfccs_no'][0])
FP1, TP1 = computeRoc(tmp1, tmp2)

tmp3, tmp4 = computeall(template, mat['mfccs_yes_nocmn'][0], mat['mfccs_no_nocmn'][0])
FP2, TP2 = computeRoc(tmp3, tmp4)

plt.plot(FP1 * 100, TP1 * 100, 'r--', FP2 * 100, TP2 * 100, '-')
plt.ylabel('True Positive Rate (%)')
plt.xlabel('False Alarm Rate (%)')
plt.title('RoC')
plt.show()
print('END')
print(FP1, TP1)