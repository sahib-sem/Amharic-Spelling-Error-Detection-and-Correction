from collections import defaultdict
import math
from edit_distance import EditDistanceSpellCheck as EditDistance
from etnltk.lang.am import clean_amharic
from amseg.amharicSegmenter import AmharicSegmenter
from etnltk import Amharic
from etnltk.lang.am import normalize
from LSTM_next_word import LSTMSpellCheck
from fastapi import HTTPException

class SpellCheck:

    '''
    use both the edit distance algorithm and next word prediction model to suggest words

    Attributes
    ----------
    edit_distance : EditDistance
        An object of the EditDistance class to suggest words using edit distance algorithm.
        use this to get non contextual suggestions of a misspelled word.
    
    next_word : LSTMSpellCheck
        An object of the LSTMSpellCheck class to suggest words using next word prediction model.
        use this to get contextual suggestions of a misspelled word.
    
    Methods
    -------
    suggestion(text)
        
        first it splits the text into sentences and words.
        then it cleans the text and normalizes the words.
        then it gets the misspelled words and their context.
        then it gets the non contextual suggestions of the misspelled words using edit distance algorithm.
        then it gets the contextual suggestions of the misspelled words using next word prediction model.
        then it combines the non contextual and contextual suggestions and returns the first 10 suggestions.
    
    next_words(text)
        first it splits the text into sentences and words.
        then it cleans the text and normalizes the words.
        then it gets the misspelled words and their context.
        then it gets the contextual suggestions of the misspelled words using next word prediction model.
        then it returns the contextual suggestions.

    '''

    def __init__(self):
        
        
        self.edit_distance = EditDistance()
        self.next_word = LSTMSpellCheck()

    def suggestion(self, text):

        doc = Amharic(text)
        words = doc.words
        sentences = doc.sentences

        words = [normalize(word) for word in words]

        sentences = [clean_amharic(s.sentence).split() for s in sentences]

        sentences = [[normalize(word) for word in sentence] for sentence in sentences]

        misspelled, contexts = self.edit_distance.misspelled_word_with_context(sentences)

        res = defaultdict(list)

        for i in range(len(misspelled)):
            
            sug = self.edit_distance.suggestion(misspelled[i])
            
        
            context = contexts[i]
            next_word_sug = self.next_word.next_word_suggestion(context)
            
            if len(next_word_sug) == 0:

                res[misspelled[i]] = sug
                continue
            

            avg_prob = (max(next_word_sug.values()) + min(next_word_sug.values())) / 2

            for word, p in sug:

                total_prob = math.log(p)

                if word in next_word_sug:
                    total_prob += math.log(next_word_sug[word])
                else:
                    total_prob += math.log(avg_prob)
                
                res[misspelled[i]].append((word, total_prob))

    
        res = {k: [val[0] for val in sorted(v, key=lambda x: x[1], reverse = True)[:10]] for k, v in res.items()}

        
        return res

    def next_words(self, text):
        doc = Amharic(text)
        words = doc.words

        if len(words) <= 2:
            raise HTTPException(status_code=400, detail="The context is too short(less than 3 words)")

        words = [normalize(word) for word in words]
        context = words[-3:]

        next_word = self.next_word.next_word_suggestion(context)

        next_word = next(iter(next_word))

        return next_word

    def next_words_top_counts(self, text, k):

        doc = Amharic(text)
        words = doc.words

        if len(words) <= 2:
            raise HTTPException(status_code=400, detail="The context is too short(less than 3 words)")

        words = [normalize(word) for word in words]
        context = words[-3:]

        next_words = self.next_word.next_word_suggestion(context)

        possible_next_words = [word for word, _ in next_words.items()][:k]
        return possible_next_words



                

                


        



