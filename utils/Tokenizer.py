from collections import defaultdict


class Tokenizer:

    def __init__(self, sentences):

        self.sentences = sentences

        self.word2idx = {}
        self.idx2word = {}
        self.vocab = defaultdict(int)

        self.build_vocab()


    def build_vocab(self):

        for sentence in self.sentences:

            for word in sentence.split():

                self.vocab[word] += 1



        self.vocab = list(self.vocab.keys())

        self.word2idx = {word:idx for idx, word in enumerate(self.vocab)}
        self.idx2word = {idx:word for word, idx in self.word2idx.items()}

    def encode(self, sentence):

        encoded = []

        for word in sentence.split():

            encoded.append(self.word2idx[word])

        return encoded

    def decode(self, encoded):

        decoded = []

        for idx in encoded:

            decoded.append(self.idx2word[idx])

        return decoded