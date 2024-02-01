
import torch
from etnltk.lang.am import clean_amharic
from utils.Tokenizer import Tokenizer
from model.LSTM_model import LSTM



class LSTMSpellCheck:

    '''
    Use a trained LSTM model to suggest next word in Amharic text given a context of 3 words.

    Attributes
    ----------
    data_path : str
        The path to the data file.
        This is the same data file used to train the LSTM model.
    
    model_path : str
        The path to the trained LSTM model. (trained on google colab) -> https://colab.research.google.com/drive/1WbaBRuUPrgAvXoOIf11iEx-mnooijwJe?usp=sharing

    tokenizer : Tokenizer
        A tokenizer object to encode and decode words to and from indices.
    
    vocab_size : int
        The size of the vocabulary.
    
    model : LSTM
        The LSTM model.
    
    Methods
    -------
    build_dataset()
        Builds the dataset and loads the model.
    
    next_word_suggestion(context)

        Returns a dictionary of suggested words and their probabilities given a context of 3 words.
        the context should be a list of 3 words. otherwise it returns an empty dictionary.
        if the context is not in the vocabulary it returns an empty dictionary.

        the size of the dictionary is of vocab_size.

    '''

    def __init__(self):

        self.data_path = './Data_and_model_pth/data.txt'
        self.model_path = './Data_and_model_pth/next_words.pth'
        self.build_dataset()
    

    def build_dataset(self):

        with open(self.data_path , 'r') as f:

            amharic_corpus = [line.strip() for line in f.readlines()]

        org_sentences = amharic_corpus

        sentences = [clean_amharic(sentence) for sentence in org_sentences]
        self.tokenizer = Tokenizer(sentences)
        embedding_dim = 10
        hidden_dim = 400
        out_size = 200
        self.vocab_size = len(self.tokenizer.vocab)
        self.model = LSTM(self.vocab_size, embedding_dim, hidden_dim, out_size)
        self.model.load_state_dict(torch.load(self.model_path)['model_state_dict'])



    def next_word_suggestion(self, context : list[str]):

        if len(context) <= 2:

            return {}
        
        for word in context:

            if not word in self.tokenizer.vocab:

                return {}

        input_sequence = [self.tokenizer.encode(" ".join(context))]

        input_tensor = torch.LongTensor(input_sequence)
        
        with torch.no_grad():
            output = self.model(input_tensor)

    
            
        
        top_k_values, top_k_indices = torch.topk(output, self.vocab_size, dim=1)
        top_k_indices = top_k_indices.squeeze().tolist()
        top_k_values = top_k_values.squeeze().tolist()
        max_val = max(top_k_values)

        top_k_values = [val / max_val for val in top_k_values]
        predicted_words = [self.tokenizer.decode([idx])[0] for idx in top_k_indices]
        
        

        top_k_values = torch.softmax(torch.tensor(top_k_values), dim=0).tolist()


        res = { word : prob for word, prob in zip(predicted_words, top_k_values)}

        return res

