#!/usr/bin/env python

from __future__ import print_function
from optparse import OptionParser

import os
import sys
import fnmatch
import datetime
import string

def my_map(func, list):
  result = []

  for (i, v) in enumerate(list):
    result.append(func(i, v))

  return result

def padd(value, width, direction):
  if direction == 'l':
    return value.ljust(width)
  else:
    return value.rjust(width)

def format_line(line, separator = '|'):
  return separator + string.join(my_map(lambda i, x: padd(x, column_width_array[i], column_padding_array[i]), line), separator) + separator

def print_super_line(line):
  if not line:
    return

  sep = format_line(map(lambda x: '-' * x, column_width_array), '+')

  print(sep)
  print(format_line(line))
  print(sep)

parser = OptionParser()
parser.add_option("-d", "--delimiter", dest="delimiter", help="column delimiter")
parser.add_option("-f", "--file", dest="file", help="input file")
parser.add_option("-p", "--padding", dest="padding", help="padding in format [column]|[column_range]{l|r}")
parser.add_option("-e", "--header", dest="header", action="store_true", help="first line is header")
parser.add_option("-o", "--footer", dest="footer", action="store_true", help="last line is footer")

(options, args) = parser.parse_args()

lines = [map(lambda y: ' ' + y + ' ', x.strip().split(options.delimiter)) for x in open(options.file).readlines()]

column_width_array = [0] * len(lines[0])
column_padding_array = ['l'] * len(lines[0])

if options.padding:
  for token in options.padding.split(','):
    direction = token[-1]
    token = token[:-1]
    if '-' in token:
      values = token.split('-')
      for i in range(int(values[0]) - 1, int(values[1]) - 1):
	if i >= len(column_padding_array):
	  continue
	column_padding_array[i] = direction
    else:
      i = int(token)
      if i >= len(column_padding_array):
	continue
      column_padding_array[i] = direction

for line in lines:
  for (i, column) in enumerate(line):
    if len(column) > column_width_array[i]:
      column_width_array[i] = len(column)

first_line = None
last_line = None

if options.header:
  first_line = lines[0]
  lines = lines[1:]
  print_super_line(first_line)

if options.footer:
  last_line = lines[-1]
  lines = lines[:-1]

for line in lines:
  print(format_line(line))

print_super_line(last_line)
