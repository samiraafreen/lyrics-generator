import lyrics
from random import randint

class MarkovLyrics:
    def __init__(self):
        self.chain = {}

    def populateMarkovChain(self, lyrics):
        for line in lyrics:
            words = line.split(' ')
            for i in range(len(words)-1):
                word, next_word = words[i], words[i+1]
                if word in self.chain:
                    self.chain[word].append(next_word)
                else:
                    self.chain[word] = [next_word]
        return
    
    def generateLyrics(self, length=50):
        n = len(self.chain)
        start_index = randint(0, n-1)
        keys = list(self.chain.keys())
        current_word = keys[start_index].title() #capitalizes the first letter of the word
        lyric_string = current_word + ' '
        for _ in range(length):
            if current_word not in self.chain:
                lyric_string += '\n'
                next_index = randint(0, n-1)
                current_word = keys[next_index]
            else:
                next_words = self.chain[current_word]
                random_index = randint(0, len(next_words)-1)
                lyric_string += next_words[random_index] + ' '
                current_word = next_words[random_index]
        return lyric_string

'''
data = ["I am avi", "I am an engineer", 'I like to code']
m = MarkovLyrics()
m.populateMarkovChain(data)
print(m.generateLyrics())
'''