import os
from static import *
import sqlite3

def a_bit_of_ipsum():
  import loremipsum
  from random import choice
  def sentence():
    return loremipsum.generate_sentence()[2]
  def word():
    return choice(loremipsum.generate_sentence()[2].split(' '))
  
  return [sentence,word]

import re
# def exclude_pattern_from_string(pattern,tag_string):
#   """ return [string without pattern, pattern] """
#   if type(pattern) == "str":
#     pattern = re.compile(pattern,re.DOTALL)
#   if not tag_string:
#     return ['','']
#   result = list(pattern.findall(tag_string))
#   if result:
#     return [result[0],pattern.sub('',tag_string)]
#   return [None,tag_string]
__stp_pattern = re.compile('[\s\n]+')
def stp(pattern):
  """
    Strip Pattern from whitespaces and new_lines
    pattern must be string
    
  """
  return __stp_pattern.sub('',pattern )
  

import difflib
def two_words_difference(wordA,wordB):
  return difflib.SequenceMatcher(None,wordA,wordB).ratio()      

def get_or_none(data,index):
  try:
    return data[index]
  except: 
    return None

def to_clip(data):
  """ TODO: figure out
      middle button copy paste 
  """
  pyperclip.copy(str(data))
  
def from_clip():
  """
    Have to install xclip
  """
  return pyperclip.paste()

def contains_word(line,word):
  if word in everything_to_list(line):
    return True
  return False


def split_list(array,keyword):
  """ split array by keyword
      keyword is not returned 

  """
  array = everything_to_list(array)
  try:
    index = array.index(keyword)
    return [array[:index],array[index+1:]]
  except ValueError:
    return [array,[]]




def weak_get(data,index):
  try:
    return data[index]
  except IndexError:
    return None

def weak_index(array,el):
  try:
    return array.index(el)
  except ValueError:
    return None
def weak_del(data,index):
  try:
    r = data[index]
    del data[index]
    return r
  except KeyError:
    return None

def weak_var(var):
  try:
    return var
  except:
    return None
  


def weak_pop(array):
  try:
    return array.pop()
  except IndexError:
    return None

def weak_to_int(string):
  try:
    return int(string)
  except ValueError:
    return None
from itertools import chain
def generator_is_not_empty(gen):
  try:
    x = gen.next()
  except StopIteration:
    return False
  return chain([x],gen)

def generator_append(gen1,gen2):
  return chain(gen1,gen2)

def list_minus_list(listA,listB):
  for i in listA:
    if not (i in listB):
      yield i


import re
__sp_split_pattern = re.compile("\s+") # have to do because of state. 
def sp_split(data):
  return  __sp_split_pattern.split(data)


__filter_numbers_pattern = re.compile('[0-9]+')
def filter_numbers(array):
  return [weak_to_int(i) for i in \
          filter(lambda x: __filter_numbers_pattern.match(str(x)),array)]
  



def list_dir(path,mode=0):
  """ list only directories
      mode == 0 # only folders
      mode == 1 # only files
      mode == 2 # both 
  """
  if mode == 0:
    def comparator(i):
      return os.path.isdir(os.path.join(path,i))
  elif mode == 1:
    def comparator(i):
      return not os.path.isdir(os.path.join(path,i))
  else:
    def comparator(i):
      return True
  for i in os.listdir(path):
    if comparator(i):
      yield i


def tags_to_list(tags):
  if tags == None:
    return []
  if type(tags) == list or type(tags) == set:
    return sorted(list(set(tags)))
  else:
    tags = set([i for i in TAG_SPLITTER.split(tags) if i])
    return sorted(tags)

def tags_to_str(tags):
  if tags == None:
    return ''
  if (type(tags) == list) or (type(tags) == set):
    tags = (i.strip() for i in tags)
    tags = sorted(set(tags))
    return tags_to_str(' '.join(tags))   # WTF !!!!! <but does not working otherwise> mystery.
  else:
    tags = set([i for i in TAG_SPLITTER.split(tags) if i])
    return ' '.join(sorted(tags))

  
def everything_to_str(smth):
  if type(smth) == str:
    return smth
  return  ' '.join(smth)

def everything_to_list(smth):
  if type(smth) == str:
    return sp_split(smth)
  return list(smth)







