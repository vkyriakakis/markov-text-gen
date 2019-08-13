import random
from argparse import ArgumentParser 
from collections import defaultdict
from sys import exit, stdin, stderr

class TextGenerator:
	''' Text generation is achieved using a Markov chain.
	 The Markov chain is modelled as a directed graph,
	 with the START state acting as the only source,  the END state
     as the only sink, and the tranisition probabilities as the graph weights.
	
	 The graph is implemented using an adjacency list,
	 which in turn is implemented as a dictionary of dictionaries.
	
	 adjacencies is a dictionary keyed by all words of the text
	 or START (the states). For each key/state, it contains
	 another dictionary indexed by the words of the text
	 that succeed the key in the text (the next states in the chain),
	 and for each of those words/next states the dictionary contains
	 the transition probability from the present state to them. '''

	# Class constant that represents the initial state
        # during the generation of the sentence (source in the graph). 
	START = ""

	# Class constant that represents the terminal state
        # during the generation of the sentence (sink in the graph).
	END = " "

	def __init__(self, file):
		self.adjacencies = defaultdict(lambda: defaultdict(int))
	
		# prev: Contains the previously encountered word or the START state,
		# initialized to the START state.
		prev = TextGenerator.START

		for line in file:
			for word in line.split():
				# If the word ends with a terminating punctuation mark,
				# ignore the mark, and treat the word as a terminating state as
				# it does not preceed another word in the current sentence.
				# So, first add a transition from word to the END state,
				# in order for the word to possibly the last of the generated
				# sentence, then prev is set to START, in order for the text model
				# to account for the fact that some words start sentences
				# more frequently than others (not all words are next states of START).
				ends_term = word[-1] in ("?", "!", ".")
				if ends_term:
					word = word[0:-1]

				# Increment the prev->word transition frequency,
				# as another one of those transitions was noted
				self.adjacencies[prev][word] += 1 
				

				if ends_term:
					self.adjacencies[word][TextGenerator.END] += 1
					prev = TextGenerator.START
				else:
					prev = word


	
	def choose_next_word(self, cur_word):
		''' Chooses the next state/word,
		 by sampling the non uniform transition probability distribution
		 of the current word/state. '''

		next_words = list(self.adjacencies[cur_word].keys())
		frequencies = list(self.adjacencies[cur_word].values())

		return (random.choices(next_words, frequencies))[0]


	
	def gen_sentence(self, limit = 0):
		''' Generates a sentence. If a positive
	        limit is not provided by the caller, the sentences grow to
		an arbitrary number of words, until the last word of a sentence/a terminal state
	        is reached. '''
		sentence = []

		cur_word = self.choose_next_word(TextGenerator.START)
		sentence.append(cur_word)

		if limit > 0:
			words_used = 1
			while words_used < limit and cur_word != TextGenerator.END:
				cur_word = self.choose_next_word(cur_word)
				sentence.append(cur_word)
				words_used += 1
		else:
			while cur_word != TextGenerator.END:
				cur_word = self.choose_next_word(cur_word)
				sentence.append(cur_word)

		return " ".join(sentence)



if (__name__ == "__main__"):
	parser = ArgumentParser(description = "Generate sentences using Markov Chains.")
	parser.add_argument("--sentences", "-s", type=int, default = 1,
		                 help = "Specify the number of sentences to be generated (> 1).")
	parser.add_argument("--limit", "-l", type=int, default = 0,
		                 help = "Specify the maximum word count of a sentence (> 1), or \
		                 enforce no limit (= 0)")
	args = parser.parse_args()


	try:
		text_generator = TextGenerator(stdin)
	except OSError as error:
		print(error.strerror, file=stderr)
		exit(1)

	if args.sentences < 1:
		print("The number of sentences must be positive.", file = stderr)
		exit(1)

	if args.limit < 0:
		print("The maximum word count must be >= 0 (0 for no maximum).", file = stderr)


	# Generate and print as many sentences as asked.
	for k in range(0, args.sentences):
		print(text_generator.gen_sentence(args.limit) + "\n")