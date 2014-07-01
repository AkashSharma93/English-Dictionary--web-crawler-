class Word:
	def __init__(self, new_word, definitions, pronunciation, synonyms, related_forms):
		self._word = new_word
		self._definitions = definitions
		self._pronunciation = pronunciation
		self._synonyms = synonyms
		self._related_forms = related_forms
	
	def get_word(self):
		"""Returns the word associated with the current Word object."""
		return self._word	
		
	def get_definitions(self):
		"""Returns the definitions associated with the word."""
		return self._definitions
		
	def get_pronunciation(self):
		"""Returns pronunciation of the word."""
		return self._pronunciation
		
	def get_synonyms(self):
		"""Returns synonyms of the word."""
		return self._synonyms
	
	def get_related_forms(self):
		"""Returns related forms of the word."""
		return self._related_forms