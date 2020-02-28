from __future__ import division
import sys, os
from random import choice


def file_reader(fname):
	questions = list()
	answers = list()
	count = 1
	info_file = open(fname)
	for line in info_file:
		if count == 1:
			new_line = line
			if line.split(" ")[0].lower() == "q:":
				new_line = line[3:]
			questions.append(new_line.split("\n")[0])
			count = count + 1
		elif count == 2:
			new_line = line
			if line.split(" ")[0].lower() == "a:":
				new_line = line[3:]
			answers.append(new_line.split("\n")[0])
			count = count + 1
		elif count == 3:
			if line != "\n":
				print "Hmmm... check file format."
				sys.exit()
			else:
				count = 1
	info_file.close()
	return questions, answers

	
def print_cards(questions, answers):
	for index, question in enumerate(questions):
		print '%dq- %s' %(index+1, question)
		print '%da- %s' %(index+1, answers[index])


def manual_input():
	print "\nWhen you have finished entering flash card info, type 'done'."
	questions = list()
	answers = list()
	question = ' '
	while question != 'done':
		question = raw_input("\nQ: ")
		if question == "done":
			break
		questions.append(question)
		answer = raw_input("A: ")
		answers.append(answer)
	print "\nWould you like to save these cards as a .txt file?"
	opWrite = raw_input('y or n > ')
	if opWrite.lower() == 'y':
		print "\nWhat would you like to name the file?"
		outputFilename = raw_input('> ').replace(".txt","")
		outputFilename = outputFilename + ".txt"
		while os.path.exists(outputFilename) == True:
			print '\nFile already exists. Would you like to overwrite?'
			overwrite = raw_input('y or n > ').lower()
			if overwrite == 'y':
				print 'Overwriting file...'
				break
			else:
				print '\nPlease type a new filename.'
				outputFilename = raw_input('> ').replace(".txt","")
				outputFilename = outputFilename + ".txt"
		with open(outputFilename, 'w') as outfile:
			for x in range(len(questions)):
				outfile.write('Q: ' + questions[x] + '\n')
				outfile.write('A: ' + answers[x] + '\n\n')
			print '\nFile \"%s\" created.' %outputFilename
		
		
	print "\nFlash card generation complete!"	
	return questions, answers

	
def test_time(questions, answers, repeat_value):
	q_backup = [x for x in questions]
	a_backup = [x for x in answers]
	if repeat_value and repeat_value != 1:
		for x in range(repeat_value-1):
			[questions.append(x) for x in q_backup]
			[answers.append(x) for x in a_backup]
	print '\n---TEST TIME---'
	if len(questions) != len(answers):
		print "Hmm... some questions or answers are missing."
	correct_count = 0
	wrong_count = 0
		
	while len(questions) != 0:
		count = -1 
		cards_left = [x for x in range(len(questions))]
		this_card = choice(cards_left)
		question = questions[this_card]
		right_answer = answers[this_card].lower()
		right_answer_words = right_answer.split(" ")
		print "\nQ:", question
		user_answer = raw_input("A: ").lower()
		user_answer_words = user_answer.split(" ")
		if user_answer_words == right_answer_words:
			print "\033[1;32mCORRECT :)\033[1;m Removing from testing pile..."
			correct_count += 1
			questions.remove(questions[this_card])
			answers.remove(answers[this_card])
		else:
			print "\033[1;31mINCORRECT!\033[1;m Let's save that one for later.."
			print "Correct Answer: %s" % answers[this_card]
			wrong_count += 1
	
	final_grade = (correct_count*100)/(correct_count+wrong_count)
	print "Testing complete!"
	print "Final Score: \033[1m%.2f%s\033[0;0m" %(final_grade, '%')
	print "Would you like to test again?"
	repeat = raw_input('y or n > ')
	if repeat == "y":
		test_time(q_backup, a_backup, repeat_value)
	else:
		print "OK, goodbye!"


if __name__ == "__main__":

        repeat_value = False				

	if len(sys.argv) >= 2:
		info_file = sys.argv[1]
		questions, answers = file_reader(info_file)
		if len(sys.argv) == 3:
			repeat_value = int(sys.argv[2])
	else:
		questions, answers = manual_input()
		
	test_time(questions, answers, repeat_value)




						


	
