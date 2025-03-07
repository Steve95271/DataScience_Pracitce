import string
import mysql.connector as pymysql
import json

printable = set(string.printable) # this is useful for the superclean() function

def superclean(s):
	# your code here, check the function call futher down to see how we'll use it
	printable
	return out

def make_category_map(prizesdata):
	# at the end of these lines, category_map should be a dict with {categoryname: id} - ids are arbitrary
	category_map = {}
	for prizedict in prizesdata['prizes']:
		cat = prizedict['category']
		# your code here
	return category_map


prizesdata = json.load(open('prize.json'))
connection = pymysql.connect(
	host='localhost',
	user='root', # replace with your username
    password='12345678',
    db='nobel_prize', # replace with your db
    charset='utf8mb4',
)


# this line turns your dictionary into a list of tuples, which we can pass to our massive insert statement further down
category_list = [(b,a) for a,b in category_map.items()]

# we are going to skip repeated laureates
seen_laureates = set()

# initialize the list of rows that we will insert into the laureates table
laureates_list = []
for prizedict in prizesdata['prizes']:
	this_category = prizedict['category']
	categoryID = # your code here
	this_year = int(prizedict['year'])
	overall_motivation = ''
	if 'overallMotivation' in prizedict:
		overall_motivation = # your code here
	if 'laureates' in prizedict:
		for laureate in prizedict['laureates']:
			laureateID = # your code here, the ID needs to be and integer!
			name = # your code here
			surname = ''
			if laureateID in seen_laureates:
				print('Duplicate laureate ID! ', laureateID, ' -- ', name,surname)
				# your code here - which python statement to go back to the beginning of the loop?
			if 'surname' in laureate:
				surname = # your code here
			motivation = # your code here
			
			# me remove non ascii chars from our strings
			name, surname, motivation, overall_motivation = superclean(name), superclean(surname), superclean(motivation), superclean(overall_motivation)
			# we initialize the list that we will use to populate our database
			this_laureate = [laureateID, name, surname, categoryID, this_year, motivation, overall_motivation]
			laureates_list.append(this_laureate)
			seen_laureates.add(laureateID)

# "Like all Python DB-API 2.0 implementations, the cursor.execute() method is designed take only one statement, 
# because it makes guarantees about the state of the cursor afterward."
# https://stackoverflow.com/questions/20518677/mysqldb-cursor-execute-cant-run-multiple-queries
try:	
	with connection.cursor() as cur:
		q = """
			CREATE TABLE ... your code here
			);
		"""
		cur.execute(q)
		connection.commit()

	with connection.cursor() as cur:
		q = """
			CREATE TABLE ... your code here
			);
		"""
		cur.execute(q)
		connection.commit()

	with connection.cursor() as cur:
		q = """
				INSERT INTO ... your code here ... VALUES (%s, %s)
		"""
		cur.executemany(q, category_list)
		connection.commit()

	with connection.cursor() as cur:
		q = """
				INSERT INTO ... your code here ... VALUES (%s, %s, %s, %s, %s, %s, %s)
		"""
		cur.executemany(q, laureates_list)
		connection.commit()

finally:
	connection.close()