import numpy as np
import pandas as pd
from sys import exit


# Implement Word recognition accuracy for fast, normal, slow speed
# ความยาวของประโยคทดสอบที่ทำให้ผลการทดสอบออกมาดี ๆ อยู่ใน range ใด ทำเป็น range เพราะมีตัวแปลที่เป็นความยากง่ายของการออกเสียงแต่ละคำในแต่ละประโยคทดสอบด้วย

def isEqual(string1, string2):

	if string1.lower() == "plus" and string2.lower() == "+":return True
	if string1.lower() == "one" and string2.lower() == "1":return True

	return string1.lower() == string2.lower()

def word_recognition_accuracy_mcs(splited_string1, splited_string2):

	correct_count = mcs({}, splited_string1, splited_string2, len(splited_string1) - 1 , len(splited_string2) - 1)
	return (correct_count, len(splited_string1), len(splited_string2), correct_count / len(splited_string1))

def mcs(mymem, splited_string1, splited_string2, i,j): # splited_string1 is the ref splited string

	if i==0:
		if splited_string1[i] in splited_string2[0:j+1]:
			return 1
		else:
			return 0 
	elif j==0:
		if splited_string2[j] in splited_string1[0:i+1]:
			return 1
		else:
			return 0
	else:
		if isEqual(splited_string1[i], splited_string2[j]):
			if (i-1,j-1) in mymem:
				return mymem[(i-1,j-1)]+1
			else:
				mymem[(i-1,j-1)] = mcs(mymem, splited_string1, splited_string2, i-1,j-1) 
				return mymem[(i-1,j-1)]+1
		else:
			if (i-1,j) in mymem:
				left = mymem[(i-1,j)]
			else:
				left = mcs(mymem, splited_string1, splited_string2, i-1,j)
				mymem[(i-1,j)] = left
			if (i,j-1) in mymem:
				right = mymem[(i,j-1)]
			else:
				right = mcs(mymem, splited_string1, splited_string2, i,j-1)
				mymem[(i,j-1)] = right
			return max(left,right)

def word_recognition_accuracy(splited_ref_sentence, splited_sentence):

	length = min(len(splited_ref_sentence), len(splited_sentence))
	correct_count = 0
	binary_list = []

	for i in range(length):
		if isEqual(splited_ref_sentence[i], splited_sentence[i]): 
			correct_count += 1
			binary_list.append(1)
		else:
			binary_list.append(0)

	for i in range(len(splited_ref_sentence) - len(binary_list)):
		binary_list.append(0)

	return (correct_count, len(splited_ref_sentence), len(splited_sentence), correct_count / len(splited_ref_sentence), binary_list)

def encoded_speed(speed):

	if speed == "slow_speed":
		return 0
	elif speed == "normal_speed":
		return 1
	elif speed == "fast_speed":
		return 2
	else:
		return np.nan

def accuracy_results(input_speed):

	global number_all_tested_words, number_all_correct_words, number_all_tested_utterance, number_all_correct_utterance, table
	results_file_content = open("results2.txt", 'r').read().splitlines()
	for i in range(0, len(results_file_content), 4):
		if results_file_content[i] == "---":
			info = results_file_content[i + 1].strip().replace(',','').split(' ')

			if input_speed == "dc" or info[3] == input_speed:
				name = info[0]
				if info[1] == "Male":
					sex = 1
				elif info[1] == "Female":
					sex = 0
				else:
					sex = np.nan
				age = int(info[2])
				speed = encoded_speed(info[3])
				english_speaking_skill_points = int(info[4])

				splited_ref_sentence = info[5:]
				ref_sentence = (' ').join(info[5:])

				if ref_sentence not in table:
					table[ref_sentence] = [[] for k in range(len(splited_ref_sentence))]

				for j in range(2,4):
					splited_sentence = results_file_content[i + j].strip().replace(',','').split(' ')
					
					wra = word_recognition_accuracy(splited_ref_sentence, splited_sentence)
					for k in range(len(wra[4])):
						table[ref_sentence][k].append(wra[4][k])
					'''
					Or comment 3 lines above, the last line of this function and create_table(table) to
					start using longest common words alogorithm (uncomment the below line) 
					'''
					# wra = word_recognition_accuracy_mcs(splited_ref_sentence, splited_sentence)

					number_all_correct_words += wra[0]
					number_all_tested_words += wra[1]

					if wra[0] == wra[1] and wra[1] == wra[2]:
						number_all_correct_utterance += 1
					number_all_tested_utterance += 1

					### For further machine learning analysis ###
					sex_col.append(sex)
					age_col.append(age)
					speed_col.append(speed)
					english_speaking_skill_points_col.append(english_speaking_skill_points)
					length_of_reference_sentence_col.append(len(splited_ref_sentence))
					number_of_correct_words_col.append(wra[0])
		
		else:
			print("results.txt has the upexpected format!, stop the running program")
			exit(0)

	print("Test with", number_all_tested_utterance, "utterances")
	print("Test with", number_all_tested_words, "words")
	print("Word recognition accuracy :", number_all_correct_words * 100 / number_all_tested_words)
	print("Utterance recognition accuracy :", number_all_correct_utterance * 100 / number_all_tested_utterance)

def create_table(dictionary):

	for rs in dictionary:
		ath_dictionnary = {}
		srs = rs.split(' ')

		for k in range(len(srs)):
			if srs[k] not in ath_dictionnary:
				ath_dictionnary[srs[k]] = []
			ath_dictionnary[srs[k]] = pd.Series(dictionary[rs][k])
		
		tmpDf = pd.DataFrame(ath_dictionnary)
		tmpDf = tmpDf[srs]
		tmpDf.to_csv(rs + ".csv", encoding = 'utf-8')

if __name__ == '__main__':

	# input_speed = input("Input speed : ")

	dic = {"Sex":pd.Series(), "Age":pd.Series()
						, "Speed":pd.Series()
						, "English speaking skill points":pd.Series()
						, "Length of reference sentence":pd.Series()
						, "Number of correct words":pd.Series()}
	sex_col = []
	age_col = []
	speed_col = []
	english_speaking_skill_points_col = []
	length_of_reference_sentence_col = []
	number_of_correct_words_col = []

	number_all_tested_words = 0
	number_all_correct_words = 0
	number_all_tested_utterance = 0
	number_all_correct_utterance = 0

	table = {}
	accuracy_results("normal_speed") # input_speed
	# print(table)
	create_table(table)

	### For further machine learning analysis ###
	dic["Sex"] = pd.Series(sex_col)
	dic["Age"] = pd.Series(age_col)
	dic["Speed"] = pd.Series(speed_col)
	dic["English speaking skill points"] = pd.Series(english_speaking_skill_points_col)
	dic["Length of reference sentence"] = pd.Series(length_of_reference_sentence_col)
	dic["Number of correct words"] = pd.Series(number_of_correct_words_col)
	df = pd.DataFrame(dic)
	# print(df.head)