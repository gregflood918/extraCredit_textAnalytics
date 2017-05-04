#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 19:45:35 2017

@author: gregflood918
"""

#Imported packages

import argparse
import sys
import os
import redactor_fx


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
parser.add_argument('--output',nargs='+',action='append',help='redact terms\
 related to specified concept')
parser.add_argument('--stats',help='output summary of \
redaction process')



#Get commmand line arguments
args = parser.parse_args()
redactor_fx.runScript(args)

