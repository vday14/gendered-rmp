import json

# r = {'is_claimed': 'True', 'rating': 3.5}
# r = json.dumps(r)
# loaded_r = json.loads(r)
# loaded_r['rating'] #Output 3.5
# type(r) #Output str
# type(loaded_r) #Output dict

# splits string into list of words
def tokenizeText(s):

	nontokens = {" ", ",", ".", ";", "!", "?"}

	s = s.lower()
	listOfTokens = s.split()

	finalListOfTokens = list()

	for token in listOfTokens:

		if len(token) > 1:

			# case 1: take out last punctuation
			if token[-1] in nontokens:
				finalListOfTokens.append(token[0:len(token)-1])

			elif len(token) >=3 and token[-2] == "'":

				if token[-1] == "s":
					finalListOfTokens.append(token[0:len(token)-2])
					finalListOfTokens.append("is")
				elif token[-1] == "m":
					finalListOfTokens.append(token[0:len(token)-2])
					finalListOfTokens.append("am")
				elif token[-1] == "d":
					finalListOfTokens.append(token[0:len(token)-2])
					finalListOfTokens.append("would")

			elif len(token) >=4 and token[-3] == "'":

				if token[-2] + token[-1] == "re":
					finalListOfTokens.append(token[0:len(token)-3])
					finalListOfTokens.append("are")
				elif token[-2] + token[-1] == "ll":
					finalListOfTokens.append(token[0:len(token)-3])
					finalListOfTokens.append("will")
				elif token[-2] + token[-1] == "ve":
					finalListOfTokens.append(token[0:len(token)-3])
					finalListOfTokens.append("have")

			# case 2: no change to word
			else:
				finalListOfTokens.append(token)

		# case 3: word is one character
		elif len(token) == 1 and token[0] not in nontokens:
			finalListOfTokens.append(token)

	return finalListOfTokens

# fxn that removes stopwords
def removeStopwords(listOfTokens):

	stopwordsstr = """
	a
	about
	all
	an
	and
	any
	are
	as
	at
	be
	been
	but
	by 
	do
	few
	from
	for
	get
	had
	have
	here
	how
	i
	if
	in
	is
	it
	its
	many
	me
	my
	none
	not
	of
	on 
	or
	our
	so
	some
	take
	the
	their
	them
	there
	they
	that 
	this
	to
	us
	was
	what
	when
	where
	which
	who
	why
	will
	with
	you
	your
	class
	great
	very
	really
	students
	exams
	lot
	material
	lecture
	lectures
	just
	would
	can
	were
	"""

	femalestr = ["her", "she", "herself", "girl", "woman", "lady"]
	malestr = ["he", "him", "his", "himself", "guy", "man"]
	stopwords = stopwordsstr.split()
	finalListOfTokens = list()
	genderTest = {"male": 0, "female": 0}

	gender = -1

	for token in listOfTokens:

		if token not in stopwords: #(stopwords or femalestr or malestr):
			if token not in femalestr:
				if token not in malestr:
					if token == "her":
						print("what")
					finalListOfTokens.append(token)
			
			# finalListOfTokens.append(token)

		if token in femalestr:
			genderTest["female"] += 1
		elif token in malestr:
			genderTest["male"] += 1

	if genderTest["female"] > genderTest["male"]:
		gender = 1
	else:
		gender = 0

	return finalListOfTokens, gender

def tags(x):
	return {
		"ACCESSIBLE OUTSIDE CLASS ": "_accessible", 
		"Amazing lectures ": "_amazingLectures",
		"BEWARE OF POP QUIZZES ": "_popQuiz",
		"Caring ": "_cares",
		"Clear grading criteria ": "_clear",
		"EXTRA CREDIT ": "_extraCredit", 
		"Get ready to read ": "_read",
		"Gives good feedback ": "_helpful",
		"GRADED BY FEW THINGS ": "_gradeFew",
		"GROUP PROJECTS ": "_groupProjects", 
		"Hilarious ": "_hilarious",
		"Inspirational ": "_inspirational",
		"LECTURE HEAVY ": "_lectures", 
		"LOTS OF HOMEWORK ": "_lotsHW",
		"Participation matters ": "_participate",
		"Respected ": "_respect",
		"Skip class? You won't pass. ": "_dontSkip",
		"SO MANY PAPERS ": "_papers",
		"TEST HEAVY ": "_tests",
		"Tough Grader ": "_toughGrader"
	}.get(x, "--------------which tag you miss??-----------")

# Create JSON object of professor terms and output to file
def getProfTerms(data):
	profs = {}
	count = 0
	femaleTerms = {}
	maleTerms = {}

	for professor in data:

		comments = ""

		for comment in data[professor]["comments"]:
			comments += comment

		comments = tokenizeText(comments)
		comments, gender = removeStopwords(comments)
		uniqueWords = dict()

		for tag, val in data[professor]["tags"].iteritems():
			word = tags(tag)
			uniqueWords[word] = val

		for word in comments:
			if word in uniqueWords:
				uniqueWords[word] += 1
			else:
				uniqueWords[word] = 1

			if gender == 0:
				if word in maleTerms:
					maleTerms[word] += 1
				else:
					maleTerms[word] = 1
			else:
				if word in femaleTerms:
					femaleTerms[word] += 1
				else:
					femaleTerms[word] = 1

		prof = {"name": data[professor]["name"],
						"gender": gender,
						"terms": uniqueWords
						}

		profs[professor] = prof

	output = json.dumps(profs, indent=4)
	f = open("profTerms.json", "w")
	f.write(output)

	termFile = open("termFile.output", "w")
	termFile.write("TOP 10 MALE TERMS:\n")
	count = 1
	for key, value in sorted(maleTerms.iteritems(), key=lambda (k,v): (v,k), reverse = True):
		termFile.write("%s %s" % (key.encode('utf-8'), value) + "\n")
		count += 1
		if count == 11:
			break
	count = 1
	termFile.write("\nTOP 10 FEMALE TERMS\n")
	for key, value in sorted(femaleTerms.iteritems(), key=lambda (k,v): (v,k), reverse = True):
		termFile.write("%s %s" % (key.encode('utf-8'), value) + "\n")
		count += 1
		if count == 11:
			break

# run if main file
if __name__ == "__main__":

	data = json.load(open('professors.json'))
	getProfTerms(data)

	