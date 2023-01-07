#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (Sanket Muchhala, Abhiram Kukkapali, Halloran Riley)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import numpy as np

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

#Code Begins

#create a dict of P(li|li-1)

#convert all the characters to a list
character_List =  list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' ")

emission = { x:0 for x in train_letters}

#Helper function to count the number of simmilar "*"s
def CompareStrings(input, complete):
    value = 0
    correct_char = train_letters[complete]
    for i in range(len(correct_char)): #loop throught the rows
        for x, y in zip(correct_char[i], input[i]):
            if x == y and x != " ": #if theyre the same and not a space
                value += 1
    
    return value

#Simple Bayes Net

simpleBayesString = ""

for letter in test_letters: #letter is a list of rows of dots
    val = 0
    best_char = ""
    for char in train_letters.keys():
        temp = CompareStrings(letter, char)
        if val < temp:
            val = temp
            best_char = char


    if(val <= 10): #if the character is just some noise make it a space
        simpleBayesString += " "
    else: #else just add the best letter to the final string
        simpleBayesString += best_char


# The final two lines of your output should look something like this:
print("the length of the string is " + str(len(list(simpleBayesString))))
print("Simple: " + simpleBayesString)










#HMM

#Initial probability
first_char_list = []
with open(train_txt_fname) as f:
    text = f.readlines()
    for line in text:
        first_bool = True
        for char in line:
            if char == " " or char not in character_List: #excluded characters
                pass
            elif first_bool: #if it is the first char
                first_char_list += [char]
                first_bool = False




#make a ditionary for the initial letter
initial_dict = { x:0 for x in train_letters}


#list for all the sentences
sentences_list = []

file = open(train_txt_fname)
for line in file:
    data = tuple([w for w in line.split()]) #split each word and punctuation
    sentences_list += [ data[0::2] ]

for i in range(len(sentences_list)):
    if sentences_list[i][0][0] not in character_List:
        pass
    else:
        initial_dict[sentences_list[i][0][0]]+=1 #get the first letter of the first word of every sentence and add it to the list

denominator = sum(initial_dict.values())
for key in initial_dict.keys():
    initial_dict[key] = initial_dict[key] / denominator





letter_list = []
with open(train_txt_fname) as file:
    data = file.read().rstrip()
for line in data:
    for i in range(len(line)):
        if line[i] in character_List:
            letter_list.append(line[i])


def NextLetterIndices(x):
    array = np.array(letter_list)
    indices = np.where(array == x)[0]
    return [x+1 for x in list(indices)]

"""this will count the occurence of eacj charcter in the text document"""
def countof(x):
    return letter_list.count(x)


#Initial list of all the transition values
transition_dict = { x : 0 for x in character_List } 

for previous in transition_dict.keys():
    list_of_after_indices = NextLetterIndices(previous)
    temp_dict = { x : 0 for x in character_List } 
    for i in list_of_after_indices: #loop through all the next indices
        if i < len(letter_list):
            temp_dict[letter_list[i]] += 1
    
    for key in temp_dict.keys():
        if countof(key) != 0:
            temp_dict[key] = temp_dict[key] / countof(key)

    transition_dict[previous] = temp_dict


hmm_string = ""

for letter in test_letters: #letter is a list of rows of dots
    val = 0
    best_char = " "
    for char in train_letters.keys():
        if hmm_string == "": #if the initial char
            temp = CompareStrings(letter, char) #get the emmision prob
        
            if val < temp:
                val = temp
                best_char = char

        else: #if not the initial
            temp = CompareStrings(letter, char) #get the emmision prob
            temp = temp * transition_dict[hmm_string[-1]][char]
            if val < temp:
                val = temp
                best_char = char
    
    hmm_string += best_char
        
print("the length of the HMM string is " + str(len(list(hmm_string))))
print("HMM: " + hmm_string) 
