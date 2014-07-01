import pickle
import os
from Word import Word
import urllib2
from bs4 import BeautifulSoup

class Dictionary:
	def __init__(self):
		try:
			words_list = open("Data/words_to_add.list", "rb")
			self._words_to_add = pickle.load(words_list)
			words_list.close()
			
		except IOError as err:
			self._words_to_add = ["dictionary"]
		
		try:
			added_words_list = open("Data/words_added.list", "rb")
			self._added_words = pickle.load(added_words_list)
			added_words_list.close()
			
			for word in self._added_words:
				if word in self._words_to_add:
					self._words_to_add.remove(word)
		
		except IOError as err:
			self._added_words = []
		
		if not os.path.isdir("Data"):
			os.mkdir("Data")
			os.mkdir("Data/RawData")
			os.mkdir("Data/DictionaryDB")
	
	def _save(self):
		words_list_file = open("Data/words_to_add.list", "wb")
		pickle.dump(self._words_to_add, words_list_file)
		words_list_file.close()
		
		words_list_file = open("Data/words_added.list", "wb")
		pickle.dump(self._added_words, words_list_file)
		words_list_file.close()
		
	def get_word(self, word):
		"""Returns a Word object for the corresponding word."""
		
		try:
			word_file = open("Data/DictionaryDB/" + word + ".dict", "rb")
			word_object = pickle.load(word_file)
			word_file.close()
		
		except IOError as err:
			self._crawl(word)
			word_object = self.get_word(word)
		
		self._save()
		return word_object
		
	def populate(self):
		"""Populates the dictionary with words by crawling dictionary.com"""
		
		for word in self._words_to_add:
			self._crawl(word)
			self._added_words.append(word)
			
		for word in self._added_words:
			if word in self._words_to_add:
				self._words_to_add.remove(word)
		
		self._added_words = []
		self._save()
	
	def _remove_punc(self, word):
		punctuations = ",.;:?!"

		for p in punctuations:
			word = word.replace(p, '')

		return word
		
	def _crawl(self, word):
		"""Finds word on dictionary.com and adds them to DB."""

		word = self._remove_punc(word)
		
		if os.path.isfile("Data/DictionaryDB/" + word + ".dict"):
			return
		
		c = raw_input("Downloading " + word + ": Continue? y/n ")
		if c == 'n':
			self._save()
			exit()
		
		#Fetch URL.
		if os.path.isfile("Data/RawData/" + word + ".html"):
			html_file = open("Data/RawData/" + word + ".html", "r")
			content = html_file.read()
			html_file.close()
			
		else:
			try:
				url = "http://dictionary.reference.com/browse/" + word
				content = urllib2.urlopen(url).read()
			except urllib2.URLError as err:
				print "Word not in database, please connect to the internet."
				exit()
		
		#Saving html content just in case I'll need to make some changes in the future.
		content_file = open("Data/RawData/" + word + ".html", "w")
		content_file.write(content)
		content_file.close()
		
		soup = BeautifulSoup(content)

		definitions = []
		for tag in soup.find_all(name='div', attrs={'class': "dndata"}):
			definitions.append(tag.text)
		
		pronunciation = soup.find_all(name='span', attrs={'class':'pron'})[1].text
		
		synonyms = ""
		for tag in soup.find_all(name='div', attrs={'id': "synonym"}):
			synonyms = tag.text
		
		synonyms = synonyms.strip()
		synonyms = synonyms.split('\n')
		
		related_forms = []
		for tag in soup.find_all(name='div', attrs={'class': 'roset'}):
			related_forms.append(tag.text)
		
		#Extract meaning, synonyms, pronunciation. Create new Word object, save the object.
		word_obj = Word(word, definitions, pronunciation, synonyms, related_forms)
		word_file = open("Data/DictionaryDB/" + word + ".dict", "wb")
		pickle.dump(word_obj, word_file)
		word_file.close()
		
		#Add all new words to words_to_add list.
		for definition in definitions:
			definition = self._remove_punc(definition)
			definition = definition.strip()
			words = definition.split(' ')
			
			for each_word in words:
				if not each_word in self._words_to_add and not os.path.isfile("Data/DictionaryDB/" + each_word + ".dict"):
					self._words_to_add.append(each_word)
		
		for each_word in synonyms:
			if not each_word in self._words_to_add and not os.path.isfile("Data/DictionaryDB/" + each_word + ".dict"):
				self._words_to_add.append(each_word)
