#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 09:22:53 2017

@author: gregflood918
"""


#Imported packages
import re
import glob
import argparse
import sys
import nltk
from itertools import chain
from nltk.corpus import wordnet
import codecs
import os
from nltk import word_tokenize, pos_tag, ne_chunk



from bs4 import BeautifulSoup



def censor(text, word):
    return ' '.join([('*' * len(word)) if x == word else x for x in text.split()])

def censor2(text, word):
           return text.replace(word, ("*"*len(word)))
           

#Function that automatically scans the current directory, looking for
#the specified file extensions.  The file extension must have the suffix
# '*.html','*.xml',or '*.txt'.  This means that the user may pass something
#like 'otherfolder/*.txt' if the user wishes to find files in another 
#directory where 'otherfolder' is the name of the directory.
def globber(fileExt):
    return glob.glob(fileExt)
    
    
#Utility function that searches a string and substitutes and *
#for the matched word. 
def redactWord(myString, redact):
    myString = str(myString)
    pattern = re.compile(r'(?<=\W)'+re.escape(redact)+'(?=\W)',re.IGNORECASE)
    myString = re.sub(pattern,'*',myString)
    return myString
    
 
#Functiont that will determine the named entities in a passed string
#and call redact words sequentially on the human names, substituting 
#a * for them.  This makes use of the nltk chunker, which performs
#basic entity extraction, but groups relevant nouns into 1 of 3 categories:
#PERSON, ORGANIZATION, or GPE (geopolitical entity)
def redactNames(myString):
    ne_tree = ne_chunk(pos_tag(word_tokenize(myString)))
    #Removing names one name at a time with a call to redactWord()
    for branch in ne_tree:
        if type(branch) is nltk.Tree and branch.label()=='PERSON':
            wordList = [i[0] for i in branch]
            wordList = ' '.join(wordList)
            myString = redactWord(myString, wordList)           
    return(myString)
    
 
#Functiont that will determine the named entities in a passed string
#and call redact words sequentially on places, substituting 
#a * for them.  This makes use of the nltk chunker, like redactNames()
#but this time matches GPEs, which we take as equivalent to a place
def redactPlaces(myString):
    ne_tree = ne_chunk(pos_tag(word_tokenize(myString)))
    #Removing names one name at a time with a call to redactWord()
    for branch in ne_tree:
        if type(branch) is nltk.Tree and branch.label()=='GPE':
            wordList = [i[0] for i in branch]
            wordList = ' '.join(wordList)
            myString = redactWord(myString, wordList)           
    return(myString)
    
    
      
#Utility function that converts the redacted string representation of
#the html file to a beautiful soup object, writes the object to a temporary
#.txt file, then uses the cupsfiler gnu utility to convert the .txt
#to a pdf.  Converting to a Beautiful Soup object preserves the formatting    
def writeHtml(htmlString,fileName):
    soup = BeautifulSoup(htmlString,'html.parser')
    html = soup.prettify("utf-8")
    fileName = str(fileName)+".pdf"
    with open("temp.txt","wb") as file:
        file.write(html)
    #convert to pdf and clean up .txt
    os.system('cupsfilter temp.txt ' + str(fileName))
    os.system('rm temp.txt')
    return
    

    
    
    

#creating arguments to parse
parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs='+',action='append',help='file extension to search')
parser.add_argument('--names',action='store_true',help='redact person names')
parser.add_argument('--dates',action='store_true',help='redact dates')
parser.add_argument('--phones',action='store_true',help='redact phone numbers')
parser.add_argument('--genders',action='store_true',help='redact genders')
parser.add_argument('--places',action='store_true',help='redact places')
parser.add_argument('--addresses',action='store_true',help='redact addresses')
parser.add_argument('--concept',nargs='+',action='append',help='redact terms\
 related to specified concept')
parser.add_argument('--stats',help='output summary of \
redaction process')



#Get commmand line arguments
args = parser.parse_args()


#Extracting the filenames to censor
fileNames = []
txtFiles = []
htmlFiles = []
for j in args.input:
    for i in j:
        if i.endswith('.html'):
            htmlFiles.extend(globber(i))
        elif i.endswith('.txt'):
            txtFiles.extend(globber(i))
        fileNames.extend(globber(i))
print(htmlFiles)
print(txtFiles)
    
#Extracting the concepts to censor
concepts = []
for j in args.concept:
    concepts.extend(j)
print(concepts)





#Dealing with html files
if len(htmlFile) > 0 :
    for file in htmlFile:
        
        f = codex.open(file,'r','utf-8')
        contents = f.read()
        f.close


            


#Note, html files will first be read in as a string using codecs.  This is
#where all substitution shall occur.  When redacting is complete, the file
#is writen using prettify





#mport nltk
#from nltk.tag.stanford import NERTagger
#st = NERTagger('stanford-ner/all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
#text = """YOUR TEXT GOES HERE"""

#for sent in nltk.sent_tokenize(text):
#    tokens = nltk.tokenize.word_tokenize(sent)
#    tags = st.tag(tokens)
#    for tag in tags:
#        if tag[1]=='PERSON': print tag
#




'''
htmlDoc.close()

html = soup.prettify("utf-8")
with open("output.html", "wb") as file:
    file.write(html)
    '''

    
'''
Codecs  - How to convert from html to pdf

   f = codecs.open("schools.html", 'r', 'utf-8') 
   j = f.read() 
   f.close()
   j = redactWords(j,'word')
   k = BeautifulSoup(j,'html.parser')
   html = k.prettify("utf-8")
   with open("output3.txt", "wb") as file:
    file.write(html)
    
os.system('cupsfilter output4.txt > output4.pdf')
os.system('rm output4.txt')    
    
'''    


'''
Using Wordnet 

synonyms = wordnet.synsets('change')
>>> set(chain.from_iterable([word.lemma_names() for word in synonyms]))

or.....
for ss in wn.synsets('small'):
>>>     print(ss.name(), ss.lemma_names())
'''

'''
How we handle multiples of the same input....
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display the square of a given number")
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print "the square of {} equals {}".format(args.square, answer)
elif args.verbosity == 1:
    print "{}^2 == {}".format(args.square, answer)
else:
    print answer
    '''