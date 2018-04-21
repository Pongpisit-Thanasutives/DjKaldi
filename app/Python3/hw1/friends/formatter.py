import json

ref_sentences={ '1':'One thing Mark Zuckerberg has consistently excelled at is destroying his enemies',
				'2':'Google Plus is no longer viewed as a threat to Facebook',
				'3':'Now Zuckerberg is turning his focus to a new enemy',
				'4':'On Thursday Facebook announced a major change to News Feed to prioritize posts from friends over posts from publishers',
				'5':"Even if it ends up helping Facebook's public image there are other risks",
				'6':'Artificial intelligence programs built by Alibaba and Microsoft have beaten humans on a reading comprehension test',
				'7':'The technology can be gradually applied to numerous applications',
				'8':'The Stanford test generates questions about a set of Wikipedia articles',
				'9':'Beijing said it wants the country to be a leader in artificial intelligence.',
				'10':'North and South Korea are discussing fielding a joint ice hockey team'}

name = 'Bone'
english_speaking_skill = 4
age = 21
output_file = open("result2.txt",'w') 
speed = "normal_speed"

with open('first-data.json', encoding = 'utf-8-sig') as data_file:
   data = json.loads(data_file.read())

c = 0
for data_point in data:
	gender = data_point["gender"]
	sentence = data_point["recog"]
	ref_sentence = ref_sentences[data_point["utter"]]
	
	if c % 2 == 0 and c != 0:
		output_file.writelines('\n')
		output_file.writelines('---')
		output_file.writelines('\n')
		output_file.writelines(name + ' ' + gender + ' ' + str(age) + ' ' + speed + ' ' + str(english_speaking_skill) + ' ' + ref_sentence)
	elif c == 0:
		output_file.writelines('---')
		output_file.writelines('\n')
		output_file.writelines(name + ' ' + gender + ' ' + str(age) + ' ' + speed + ' ' + str(english_speaking_skill) + ' ' + ref_sentence)
	
	output_file.writelines('\n')
	output_file.writelines(sentence)

	c += 1