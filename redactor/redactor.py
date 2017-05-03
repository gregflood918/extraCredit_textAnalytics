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
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup



#Censorship dictionary:  Each time a specfic censorship activity takes place,
#we will increment the appropriate spot in the dictionary.  This will be
#used for the stats argument
myKeys=['names','genders','dates','places','addresses','phones','concept']
censorship_dict={key: 0 for key in myKeys}


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
    

#Utility function that will substitute 5 asteriks for a sentence if the 
#sentence contains a concept.  This is only used in the remove concept
#argument   
def redactSentence(myString,redact):
    sentences = nltk.sent_tokenize(myString)
    pattern = re.compile(r'(?<=\W)'+re.escape(redact)+'(?=\W)',re.IGNORECASE)
    for i in range(len(sentences)):
        if re.search(pattern,sentences[i]):
            sentences[i] = '*****'
            censorship_dict['concepts']+=1
    myString = ' '.join(sentences) #Might slightly alter format, but meh 
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
            censorship_dict['names']+=1
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
            censorship_dict['places']+=1
    return(myString)
    

#Function that will redact ideas/themes form the text.  The approach
#is to find the synonyms using wordnet for the idea.  Then each idea
#will be Lemmatized, getting it to its root word.  Next, the html/txt
#string will be tokenized, storing the unique tokens in a set.  This 
#set will be used to create a dictionary where the key is the lemmatized
#version of each token, and the value is the token itself.  Then, the 
#synonyms will be compared to the set, to see if they  are contained within.
#if they are, they will be mapped to the word form the text, and subsequently
#fed into the redactWord() function
def redactIdeas(myString,idea):
    wn = WordNetLemmatizer()
    tokens = word_tokenize(myString)
    token_keys = [wn.lemmatize(i) for i in tokens]
    word_dict = dict(zip(token_keys,tokens))
    #Now that we have a dictionary of lemmatized words to actual words,
    #We can use wordnet to find synonyms.  This will suffice for finding
    #words that fit within an "idea"
    synonyms = wordnet.synsets(idea)
    synonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    for word in synonyms:
        if word in word_dict.keys():
            actualWord = word_dict[word]
            myString = redactSentence(myString,actualWord)
    return myString


#Function to replace 10 digit phone numbers with an asterik.  We will
#assume that a 7 digit phone number is sufficiently anonymous given the
#number of area codes in the United States     
def redactPhoneNum(myString):
    pattern = re.compile(r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}')
    censorship_dict['phones']+=len(re.findall(pattern, myString)) #get counts
    myString = re.sub(pattern,'*',myString)
    return myString
    

#Very simple function that will iterate through a list of gender specfic 
#words and pronouns, redacting each sequentially. 
def redactGenders(myString):
    female = ['female','girl','woman','her','she','her','women']
    male = ['male','boy','man','his','him','men','he']
    for i in female:
        pattern = re.compile(r'(?<=\W)'+re.escape(i)+'(?=\W)',re.IGNORECASE)
        censorship_dict['genders']+=len(re.findall(i, myString))
        myString = re.sub(pattern,'*',myString)
        print(myString)
    for i in male:
        pattern = re.compile(r'(?<=\W)'+re.escape(i)+'(?=\W)',re.IGNORECASE)
        #pattern = re.compile(r'(?<=[^|\W+])'+re.escape(i)+'(\W+|$)',re.IGNORECASE)
        censorship_dict['genders']+=len(re.findall(i, myString))
        myString = re.sub(pattern,'*',myString)
        print(myString)
    return myString
    
    
#Function to redact dates of the following formats:
#dd/mm/yyyy,dd-mm-yyyy dd.mm.yyyy where each day and month
#can be reduced to a single digit, and the year can be reduced to 2 digits
#Also matches dates of the form January, XX, XXXX   
def redactDates(myString):  
    pattern = re.compile(r'[0-9]{1,2}(\/|-|\.)[0-9]{1,2}(\/|-|\.)[0-9]{2,4}')
    pattern2 = re.compile(r'[January|February|March|April|May|June|July|'
                             'August|September|October|November|December] '
                             '[0-9]{1,2}[\s|,]{0,1} [0-9]{4}')
    censorship_dict['dates']+=len(re.findall(pattern,myString))
    censorship_dict['dates']+=len(re.findall(pattern2,myString))
    myString = re.sub(pattern,'*',myString)
    myString = re.sub(pattern2,'*',myString)
    return myString

    

#Function to redact dates of the following format:
#800 SE 20 AVENUE #603, DEERFIELD BEACH    
#The regex below is slightly altered from a regex found on stack
#exchange: http://stackoverflow.com/questions/9397485/regex-street-address-match
def redactAddresses(myString):
    pattern = re.compile(r'\s*([0-9]*)\s((NW|SW|SE|NE|S|N|E|W))?(.*)'
                               '((NW|SW|SE|NE|S|N|E|W))?((#|APT|BSMT|'
'BLDG|DEPT|FL|FRNT|HNGR|KEY|LBBY|LOT|LOWR|OFC|PH|PIER|REAR|RM|SIDE|SLIP|'
'SPC|STOP|STE|TRLR|UNIT|UPPR|ST|PL|\,)[^,]*)(\,)([\s\w]*)')
    censorship_dict['addresses']+=len(re.findall(pattern,myString))
    myString = re.sub(pattern,'*',myString)                         
    return myString
    

#Reads in an html file to a single string to return
def readHtml(htmlFile):
    f = codecs.open(htmlFile,'r','utf-8')
    contents = f.read()
    f.close
    return contents


#Reads in a .txt file to a single string to return
def readTxt(txtFile):
    f = codecs.open(txtFile, 'r','utf-8')
    contents = f.read()
    f.close
    return contents
    
      
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
        file.close()
    #convert to pdf and clean up .txt
    os.system('cupsfilter temp.txt >' + str(fileName))
    os.system('rm temp.txt')
    return
    

#Function that will write the redaction statistics to the specified 
#location. The statistics consist of the number of redactions in the order
#show.  Note that there is overlap between redactions: editing a concept 
#removes entire sentences that might contain other terms that would be
#redacted via other flags.  So this number will change for each individual
#component depending on which arguments are passed    
def writeStats(location):
    output = 'Statistical Summary\nThe number or redactions in each category are listed below:\n'
    for j in myKeys:
        output += str(j) + ': ' + str(censorship_dict[j]) + '\n'
    location = location.lower()
    if location == 'stderr':
        sys.stderr.write(output)
    elif location == 'stdout':
        sys.stdout.write(output)
    else:
        with open(str(location)+'.txt',"w") as file:
            file.write(output)
            file.close()
        
        
#Utility function that converts the writes the redacted string representation
#of a temporary .txt file, and then writes it to a pdf
def writeTxt(txtString, fileName):
    fileName = str(fileName)+".pdf"
    with open("temp.txt","w") as file:
        file.write(txtString)
        file.close()
        #convert to pdf and clean up .txt
    os.system('cupsfilter temp.txt >' + str(fileName))
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
zipping up a dictionary

keys = ['a', 'b', 'c']
>>> values = [1, 2, 3]
>>> dictionary = dict(zip(keys, values))
>>> print(dictionary)


So we need to lemmatize each of the synonyms from wordnet

Then we need tokenize the html/txt

We need to make a set of the tokenized html/txt


Then we need to create a dictionary with keys as lemmatization of tokens
from html/txt and values as the tokens themselves 

Then iterate throgh each of the synonyms, checking if the set contains
the lemma of the synoym.  If it does, then get the word from the key
value map, the remove that word

Then we need to return


 '''





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
    print(ss.name(), ss.lemma_names())
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