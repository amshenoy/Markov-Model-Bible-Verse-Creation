'''
Markov model to generate Bible verse from the Gospel of John
'''

import numpy as np
import pandas as pd
from random import randint

#Read the csv into a dataframe
df = pd.read_csv('./gospel_of_john.csv', encoding='utf-8')

#Define function to get the average number of words per line
def avg_line_length(datfram):
    lengths = []
    punc = [",", ".", "?", "!", ";", ":"]
    for row in datfram.verse:
        #Replace punctuation
        for mark in punc:
            row.replace(mark, " " + mark + " ")
        #Get length of of verse in terms of words and punctuation
        l = len(row.split())
        lengths.append(l)
    return int(round(np.mean(lengths)))
        
#Store verses as 1 text block, with a space between sentences
verse = df.verse
gospel_text = ""
for i, v in enumerate(verse):
    if i == 1:
        gospel_text += v.strip()  #Don't put a space before first sentence
    else:
        gospel_text += " " + "".join(v.strip())
#print(gospel_text)

#Define function to create a dictionary of dictionaries for each word
def create_word_dict(text):
    #Remove quotation marks
    text = text.replace("\"", "")
    #Specify punctuation marks so that they will be treated as words
    punc = [",", ".", "?", "!", ";", ":"]
    for mark in punc:
        text = text.replace(mark, " " + mark + " ")
    wordlist = text.split(" ")  #Parse words in gospel into list of words
    wordlist = [word for word in wordlist if word != ""]  #Remove empty word spaces
    #Create a word dictionary with dicionaries for each word to list the words following it and the frequncy of times each one follows the word
    worddict = {}
    for word in range(1, len(wordlist)):
        #If the current word is not in the word dict, then add it as a key with a blank dict as the value
        if wordlist[word-1] not in worddict:
            worddict[wordlist[word-1]]={}
        #If the current word is not in the values dict for the current word, then add it to the values dict for the current word with a value of 0 
        if wordlist[word] not in worddict[wordlist[word-1]]:
            worddict[wordlist[word-1]][wordlist[word]] = 0
        worddict[wordlist[word-1]][wordlist[word]] += 1  #Increase the value of the current word every time it is found (a wordcount)
    return worddict

#Define a function to total the frequency values of all words appearing after the specified word in the input 'wordList'
def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum

#Define a funtion to pull one of the words following the specified word in wordList, in proportion to how often that word follows the specified word
def getRandomWord(wordList):
    randIndex = randint(1, wordListSum(wordList))  #Random value between 1 and the sum of the frequencies of all words appearing after the specified wod in the input 'wordList'
    #Loop through words and values appearing after the specified word in wordList, subtracting each word's value from randint
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:  #When enough words have been subtracted, randIndex will be <= 0, and the word at that index is returned.  Words will always be returned in proportion to their frequncy.
            return word

#Build word dictionary
gospel_word_dict = create_word_dict(gospel_text)

#Generate a Markov Chain text string
def markov_text(starting_word):
    string_length = avg_line_length(df)
    chain = ""
    for i in range(0, string_length):
        chain += starting_word + " "
        starting_word = getRandomWord(gospel_word_dict[starting_word])
    chain += "."
    return chain

print(markov_text('In'))  #Example

