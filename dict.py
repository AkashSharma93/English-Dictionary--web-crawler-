import dictionary

def display(word_obj):
	print "\n\n" + word_obj.get_word().upper()
	
	for p in word_obj.get_pronunciation():
		print p, 
	
	print "\n\n"
	
	for definition in word_obj.get_definitions():
		print "* " + definition
		
	print "\n\nSynonyms\n"
	
	for synonym in word_obj.get_synonyms():
		print "* " + synonym
		
	print "\n\nRelated Forms\n"
	
	for form in word_obj.get_related_forms():
		print "* " + form
	
	print "\n---------------------------\n"

dict = dictionary.Dictionary()

print "\n\nSimple Dictionary v1.0 by Akash Sharma. All credit goes to dictionary.com for the words."
menu = "\n\n1. Search.\n2. Populate dictionary.\n3. Exit!\n"

while True:
	choice = input(menu)
	if choice == 1:
		display(dict.get_word(raw_input("Enter word: ").lower()))
		
	elif choice == 2:
		dict.populate()
		
	elif choice == 3:
		break
		
print "\n\nThank you for using. :)"
