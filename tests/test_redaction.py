#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 20:40:59 2017

@author: gregflood918
"""

'''
Test file to test that the redaction functions from redactor_fx.py
are working properly

'''

import os
import pytest
import glob
from redactor import redactor_fx

#Test redactWord() against a known string
def test_redactWord():
    testString = 'This is a test'
    result = redactor_fx.redactWord(testString,'is')
    assert result == 'This * a test'
 
#Test redactSentence() against a known string
def test_redactSentence():
    testString = 'This is a test.'
    result = redactor_fx.redactSentence(testString,'is')
    assert result == '*****'

#Test redactNames() against a known string with a name in it.
#The function will recognize that we have a name in the string.   
def test_redactNames():
    testString = "My name is Greg Flood."
    result = redactor_fx.redactNames(testString)
    assert result == "My name is *."

#Test redactPlaces() against a known string with a place in it
#The function will recoginize that this is a place    
def test_redactPlaces():
    testString = "The United States of America."
    result = redactor_fx.redactPlaces(testString)
    assert result == 'The * of *.'

#Test redactIdeas() against a general idea.  The function will look
#for synonyms and redact the entire sentence if a synonym for the passed
#word is present.  Note that the passed word isn't present in the test string.
def test_redactIdeas():
    testString = "The children went to the children's room"
    result = redactor_fx.redactIdeas(testString,'kids')
    assert result == '*****'

#Test redactGenders() against a known string with gender specific
#words in it.    
def test_redactGenders():
    testString = "The men and women went to the girl's house"
    result = redactor_fx.redactGenders(testString)
    assert result == "The * and * went to the *'s house"

#Test redactDates() against a known string with a date in it    
def test_redactDates():
    testString = "It was 3/19/2003."
    result = redactor_fx.redactDates(testString)
    assert result == "It was *."

#Test redactAddresses() against a known string with an address in it.   
def test_redactAddresses():
     testString = '2723 NW 32 PL, OKLAHOMA CITY' 
     result = redactor_fx.redactAddresses(testString)
     assert result == '*'
    
    
    
    