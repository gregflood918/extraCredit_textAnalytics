#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Greg Flood
CS 5970 Text Analytics



Tests for redactor_fx
This test file is focused
"""

import os
import pytest
import glob
from redactor import redactor_fx

#Test that the glob file properly identifies the passed file extension
def test_globber():
    assert 'setup.py' in set(redactor_fx.globber('*.py'))

#Test that a text file can be read in properly with readTxt()    
def test_readTxt():
    os.system('touch test.txt')
    os.system('echo "test" >> test.txt')
    line = redactor_fx.readTxt('test.txt')
    os.system('rm test.txt')
    assert line == 'test\n'
    
#Test that an html file can be read in properly with readHtml()
def test_readHtml():
    os.system('touch test2.html')
    os.system('echo "test" >> test2.html')
    line = redactor_fx.readHtml('test2.html')
    os.system('rm test2.html')
    assert line == 'test\n'
    
#Test that an html file can be converted to pdf with writeHtml()
def test_writeHtml():
    redactor_fx.writeHtml('test','test')
    test = os.path.isfile("test.pdf")
    os.system('rm test.pdf')
    assert test
    
#Test that a txt file can be converted to pdf with writeTxt()   
def test_writeTxt():
    redactor_fx.writeTxt('test','test2')
    test = os.path.isfile("test2.pdf")
    os.system('rm test2.pdf')
    assert test




