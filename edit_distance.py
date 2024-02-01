
import random
from etnltk.lang.am import normalize


class EditDistanceSpellCheck:


    '''
    This class is used to check spelling errors in Amharic text using edit distance algorithm 

    Attributes
    ----------
    probs : dict
        A dictionary of words and their probabilities.

    all_letters : set
        A set of all Amharic letters.

    dictionary : dictionary
        A dictionary of words and their frequencies.

    Methods
    -------

    edits(word, distance = 1) 
        Returns a set of all possible words with edit distance of 1 and from the misspelled of distance 1 it picks 5 randomly to do second edit distance

    suggestion(word)
        Returns a list of tuples of suggested words and their probabilities.
    
    suggestion_from_text(text)
        Returns a list of lists of tuples of suggested words and their probabilities for each word in the text that is misspelled.
    
    misspelled_from_text(text)
        Returns a list of misspelled words in the text.

    misspelled_word_with_context(sentences)
        Returns a list of misspelled words and their context in the text( previous 3 words before the misspelled word)

    '''
    
    def __init__(self):
        
        self.build_dataset()
        
    def split(self, word):
        return [(word[:i], word[i:]) for i in range(len(word) + 1)]
    
    def delete(self, word):
        return [l + r[1:] for l,r in self.split(word) if r]
    
    def insert(self, word):
        return [l + c + r for l, r in self.split(word) for c in self.all_letters]
    
    def swap(self, word):
        return [l + r[1] + r[0] + r[2:] for l, r in self.split(word) if len(r)>1]
    
    def replace(self, word):
        return [l + c + r[1:] for l, r in self.split(word) if r for c in self.all_letters]

    def get_all_edits(self, word):
        
        return self.delete(word) + self.insert(word) + self.replace(word) + self.swap(word)
    
    def edits(self, word, distance = 1):
        
        res = []
        
        res = [w for w in self.get_all_edits(word)]
        misspelled = [w for w in res if w not in self.dictionary]

        res = [w for w in res if w in self.dictionary]

        second_edits = []
    
        misspelled = random.sample(misspelled, min(5, len(misspelled)))

        second_edits = [w for word in misspelled for w in self.get_all_edits(word) if w in self.dictionary]
        
        res.extend(second_edits)

        return set(res)
    
    def suggestion(self, word):


        
        if word in self.dictionary or word == '':
            
            return []
        
        
        word_edits = self.edits(word)
        
        suggestions = [(w, self.probs[w]) for w in word_edits if w in self.probs]


        
        
        return sorted(suggestions , key = lambda x:-x[1])
    
    def is_amharic_word(self, word):
    
        for char in word:
            if not (ord('\u1200') <= ord(char) <= ord('\u137F')):
                return False

        return True
    
    def build_dataset(self):

        with open('./Data_and_model_pth/dictionary.txt', 'r') as f:
            file = f.readlines()
            data = [line.rstrip() for line in file]

        
        word_frequency = dict([(word.split()[0] , int(word.split()[-1])) for word in data])
        word_frequency = dict([(normalize(word), cnt) for word, cnt in word_frequency.items() if self.is_amharic_word(word)])

        total = float(sum(word_frequency.values()))

        probs = {word:(cnt/ total) for word, cnt in word_frequency.items()}
        
        self.probs = probs
        self.all_letters = ''.join(chr(x) for x in range(0x1200, 0x139A))
        self.dictionary = set(word_frequency.keys())
    
    def misspelled_from_text(self, words):

        misspelled = []

        for word in words:
            if word not in self.dictionary:
                misspelled.append(word)

        return misspelled
    
    def suggestion_from_text(self, words):
            
        


        suggestions = []

        for word in words:
            if word not in self.dictionary:
                suggestions.append(self.suggestion(word))

        return suggestions

    def misspelled_word_with_context(self, sentences) -> list[list[str]] | list[str]:
        
        contexts , misspelled_words = [], []
    
        for s in sentences:

            for i, word in enumerate(s):

                if word not in self.dictionary:
                    
                    context = s[max(0, i - 3):i] 
                    misspelled_words.append(word)
                    contexts.append(context)
        
        return misspelled_words, contexts
    

