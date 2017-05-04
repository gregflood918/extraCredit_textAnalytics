Greg Flood
CS 5970 - Text Analytics
University of Oklahoma

Extra Credit Assignment 


***************************************************************************
***************************************************************************
DESCRIPTION:

This extra credit project seeks to redact sensitive items from .html and
.txt documents based on user supplied command line arguments.  All of the
edited files will be copied to unique pdf files and saved in a new 
directory.  Within these files, the specified words/themes will be redacted
and replaced with a * character.

A detailed discussion of the features, as well as instructions
for running the simulation are below



***************************************************************************
***************************************************************************
Language : Python 3



***************************************************************************
***************************************************************************
Instructions:

To run the redactor on a file, navigae to the extraCredit_textAnalytics
directory and run the following command:

python3 redactor/redactor.py [args]

Where [args] refers to the following command line arguments

--input [file]  :   File to be parsed.  Can accept multiple input files and can 
                    wildcard characters such as *.  For example, '*.html' will 
                    look for all .html files in the current working directory.  
                    Likewise 'files/*.txt' will look for all .txt files in 
                    the files/ directory.
          
--output [file] :   Location to output pdf files. If an argument is not 
                    supplied, then the pdf files will not be saved. Program 
                    will trim off the / character if supplied
        
--names         :   Redacts all names of people if passed

--genders       :   Redacts all gender specific words

--dates         :   Redacts all dates from the files

--places        :   Redacts all locations from the files

--addresses     :   Redacts all addresses from file

--phones        :   Redacts all phone numbers from the file

--concept [word]:   Redacts all sentences that share a 'concept' related to
                    the passed arguments
                    
--stats [args]  :   Accepts a single argument from either a file name, stdout
                    or stderr.  Statistics will be printed to the specified 
                    location.  The statistics consist of the number of 
                    redactions made in the file.
  
An example:

python3 redactor/redactor.py --input *.html --output newFiles --names --gender\
--concept kids --stats stdout

This argument will redact all .html files in the current working directory and
output the edited files to a new directory title 'newFiles'.  All names,
genders, and words related to the concept 'kids' will be replaced with a * or
a ***** if the full sentence is redacted (for concepts).

The file structure for the project:

    redactor/
        redactor.py
        redactor_fx.py
        __init__.py
    setup.py
    setup.cfg
    tests/
        test_io.py
        test_redaction.py
    requirements.txt

The redactor.py file consists of the command line argument parser, which
is passed to redactor_fx.py when the script runs.  This decision was made
to facilitate testing.

The pytest runner can be called with the following command:

python3 setup.py test

There are 13 total tests.

The implemenation details for each flag will be discussed below
                    
***************************************************************************
***************************************************************************
Discussion:

The methodology by which each flag redacts its subject is discussed
sequentially.  The specific functions used will be listed in the next section,
with another to follow discussing the tests.  

In general, both html files and txt files are treated identically in how
they are censored, with the only difference being how they are read into
the system (BeautifulSoup is used for html).  Both .txt and .html files are
read into a string, which is then manipulated and ultimately written back
to a pdf using the cupsfilter gnu utility.  Html files undergo an additional 
step where they are converted back to html formatting before writing. The
goal is to preserve the exact structure of the original .html and .txt files,
but just have them moved to a pdf format.

Some of the functions use a utility function called "redactWord", which uses
regular expressions to remove a specific passed word.  How these words are 
passed is the subject of the individual functions that correspond to the flags.
There is one function specific to each flag. Each function accepts at least 
a string, which will contain the text to be redacted.  This string should
be the entire contents.

--names
Names are identified using the nltk named entity chunker.  After tokenizing
and tagging the entire file (for POS), the ne_chunk function is called, which
identifies three categories of named entities "PERSON", "GPE" (global
political entity), and "ORGANIZATION".  The words corresponding to the "PERSON"
tag are pulled out and sequentially passed to redactWord()


--genders
Genders are redacted by comparing the contents of each file to the a list
of male and female gender specific words, which are sequentially redacted.

--dates
Dates are redacted by comparing the contents of each file to a regex pattern
designed to catch dates with the following formats: dd/mm/yyyy,dd-mm-yyyy 
dd.mm.yyyy, or long form months like January, XX, XXXX

--places
Implementation is identical to names, using the ne_chunk function from nltk,
but pulling out "GPE" tags instead of "PERSON" (a geopolitical entity is
a place: ex- United States)

--addresses
Compares a regular expression pattern to the contents of the file and
redacts accordingly.  The regex pattern can be found in the code, but it is
designed to find addresses of the form ### [NW|SW|...] STREET NAME, CITY
note that this doesn't idenify states, as the places filter would do that.

--phones
Compares a regular expression patter to the contents of the file and redacts
accordingly.  It is designed to catch standard US 10 digit phone numbers
with the followin formats: (###)###-#### or ###-###-####

--ideas
This function uses the Wordnet package from NLTK.  First, this argument
tokenizes all the words form the passed file.  These tokens are then
lemmatized using the wordnet lemmatizer (wn.lemmatize(word)) which gets
the root word of the identified word.  A dictonary is created mapping root
words to actual word in the text.  Next, wordnet.synsets(idea) is used to
get the synonyms for the passed idea, which are then lemmatized. The synonyms
to the concepts are then compared to the dictionary containing lemmatized words,
which then returns the words to be removed from the text.  Since we are asked
to redact entire sentences containing an idea, a separate utility, 
'redactSentences' is used, which takes advantage of the nltk tokenizer.

--stats
Function that accepts argument specifying location to print statistics.
The statistics are simply the number of redactions made across all files 
cumulatively.  This is implemented via updates to a dictionary, which is
incremented whenver an edit is made.


***************************************************************************
***************************************************************************
Functions:

There are no functiosn in redactor.py, just a script to run the commmand
line interface.  This script call the runScript() function from 
redactor_fx, which contains calls to all the relevant functions in the
redactor_fx.py file, where all the functions are stored.

Functions in redactor.fx:


def globber(fileExt):
Function that automatically scans the current directory, looking for
the specified file extensions.  The file extension must have the suffix
'*.html','*.xml',or '*.txt'.  This means that the user may pass something
like 'otherfolder/*.txt' if the user wishes to find files in another 
directory where 'otherfolder' is the name of the directory. 
    

def redactWord(myString, redact):
Utility function that searches a string and substitutes and *
for the matched word. 
    
 
def redactSentence(myString,redact):
Utility function that will substitute 5 asteriks for a sentence if the 
sentence contains a concept.  This is only used in the remove concept
argument              
 

def redactNames(myString):
Functiont that will determine the named entities in a passed string
and call redact words sequentially on the human names, substituting 
a * for them.  This makes use of the nltk chunker, which performs
basic entity extraction, but groups relevant nouns into 1 of 3 categories:
PERSON, ORGANIZATION, or GPE (geopolitical entity)
 

def redactPlaces(myString):
Functiont that will determine the named entities in a passed string
and call redact words sequentially on places, substituting 
a * for them.  This makes use of the nltk chunker, like redactNames()
but this time matches GPEs, which we take as equivalent to a place
    

def redactIdeas(myString,idea):
Function that will redact ideas/themes form the text.  The approach
is to find the synonyms using wordnet for the idea.  Then each idea
will be Lemmatized, getting it to its root word.  Next, the html/txt
string will be tokenized, storing the unique tokens in a set.  This 
set will be used to create a dictionary where the key is the lemmatized
version of each token, and the value is the token itself.  Then, the 
synonyms will be compared to the set, to see if they  are contained within.
if they are, they will be mapped to the word form the text, and subsequently
fed into the redactWord() function


def redactPhoneNum(myString):
Function to replace 10 digit phone numbers with an asterik.  We will
assume that a 7 digit phone number is sufficiently anonymous given the
number of area codes in the United States 
    

def redactGenders(myString):
Very simple function that will iterate through a list of gender specfic 
words and pronouns, redacting each sequentially. 
    
    
def redactDates(myString):  
Function to redact dates of the following formats:
dd/mm/yyyy,dd-mm-yyyy dd.mm.yyyy where each day and month
can be reduced to a single digit, and the year can be reduced to 2 digits
Also matches dates of the form January, XX, XXXX   

    
def redactAddresses(myString):
Function to redact dates of the following format:
800 SE 20 AVENUE #603, DEERFIELD BEACH    
The regex below is slightly altered from a regex found on stack
exchange: http://stackoverflow.com/questions/9397485/regex-street-address-match


def readHtml(htmlFile):
Reads in an html file to a single string to return


def readTxt(txtFile):
Reads in a .txt file to a single string to return
    

def writeHtml(htmlString,fileName):    
Utility function that converts the redacted string representation of
the html file to a beautiful soup object, writes the object to a temporary
.txt file, then uses the cupsfiler gnu utility to convert the .txt
to a pdf.  Converting to a Beautiful Soup object preserves the formatting   


def writeStats(location):
Function that will write the redaction statistics to the specified 
location. The statistics consist of the number of redactions in the order
show.  Note that there is overlap between redactions: editing a concept 
removes entire sentences that might contain other terms that would be
redacted via other flags.  So this number will change for each individual
component depending on which arguments are passed    

def writeTxt(txtString, fileName):
Utility function that converts the writes the redacted string representation
of a temporary .txt file, and then writes it to a pdf


def runScript(args): 
Function that drives the program.  Accepts the parsed arguments object
from redactor.py and manages the flow of the program.
   

***************************************************************************
***************************************************************************
Tests:

There are two test files, test_io.py which tests the reading and writing
functions from redactor_fx.py and test_redaction.py, which tests the 
redaction files from redactor_fx.py

In general, all the tests create either a dummy file or a dummy string. In
the redaction cases, a dummy string containing a known pattern to be redacted
is passed to the redaction functions described above.  The test is passed
if the returned value is equal to the expected redaction.

test_io.py

def test_globber():
Test that the glob file properly identifies the passed file extension

def test_readTxt():
Test that a text file can be read in properly with readTxt()    
  
def test_readHtml():
Test that an html file can be read in properly with readHtml()

def test_writeHtml():
Test that an html file can be converted to pdf with writeHtml()
  
def test_writeTxt():
Test that a txt file can be converted to pdf with writeTxt()   





test_redaction.py

def test_redactWord():
Test redactWord() against a known string

def test_redactSentence():
Test redactSentence() against a known string

def test_redactNames():
Test redactNames() against a known string with a name in it.
The function will recognize that we have a name in the string.   

def test_redactPlaces():
Test redactPlaces() against a known string with a place in it
The function will recoginize that this is a place 

def test_redactIdeas():
Test redactIdeas() against a general idea.  The function will look
for synonyms and redact the entire sentence if a synonym for the passed
word is present.  Note that the passed word isn't present in the test string.

def test_redactGenders():
Test redactGenders() against a known string with gender specific
words in it.   

def test_redactDates():
Test redactDates() against a known string with a date in it    

def test_redactAddresses():
Test redactAddresses() against a known string with an address in it.   

    


***************************************************************************
***************************************************************************
Bugs:

Please be aware of the directory in which you are making a call to 
redactor.py with respect the files you are trying to redact.  