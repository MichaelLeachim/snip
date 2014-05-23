
#######  COMPLETE WITH REGEX SECTION
# Reason:
#   it is too complex and blundering to write atuocomplete
#   parsing for each function
# How it works:
#   bind(func_list,regexp,function)  
#   def function(ct,regexp_matchee ... regexp_matcheeN)
#   ct == context
#   ct.cur_dir
#   ct.sort
#   ct.on
#   ct.etc
#   worker(line,func_list,ct)
#     find line-corresponding-regexp
#     eval regexp-corresponding-function
#       with regexp-groups
#       with specified ct
#       return result
# Todo:
#   make this python package and distribute it
#   make it @decorable
# SO Go on, write some autocomplete_functions
######### SETUP SUBSECTION ########
import re
import utils as u
from collections import OrderedDict
class manage_ContextObject:
  pass

ct  = manage_ContextObject()
clist  = [] # complete list
colist = [] # commands list
def manage_bind(func_list,regexp,function):
  # :TESTED:
  """
  regexp might be str or  re_instance
  function must accept regexp groups and one ct param
  """
  if type(regexp) == str:
    regexp   = re.compile(regexp)
    
  datastruct = (regexp,function)
  func_list.append(datastruct)
  return func_list

def manage_worker(line,func_list,ct):
  """Worker finds suitable function from func list
     It passes result from parsing to this list, 
     and  appends arguments from params to it
  """
#  params = list(params)
  for k,v in func_list:
    if k.match(line):
      #print k,line
      #print 'fuck'
      #data = u.weak_get(k.findall(line),0) or []
      data  = k.findall(line)
      data.append(ct) # push-left like
#      print v(*data)
      return v(*data)

def dbind(clist,regexp):
  # :TESTED:
  " decorator for manage_bind function "
  def func_decorator(func):
    manage_bind(clist,regexp,func)
    def func_wrapper(*args,**kwargs):
      return func(*args,**kwargs)
    return func_wrapper
  return func_decorator



########## FUNCTION SUBSECTION ########
# EXAMPLE
# "^mv ([0-9\*\s]*) to (.+)$" complete_cd_free(nodes,tags,ct)
# "^mv ([0-9\*\s]*)$"         complete_ls(nodes,ct)
# "^cd (.+)$"                   complete_cd
# "^edit-as-one ([0-9\s\*]*)$"  edit_as_one(nodes,ct)
# ct must implement
#   ct.c       == cursor
#   ct.cur_dir == [tagA,tagB,tagC,tagN]
#   ct.sort    == 'by_length | by_name '

@dbind(clist,'^cd (.+[^\s])$')
def complete_cd_with_word(path,ct):
  # :TESTED:
  c,cur_dir,sort = ct.c,ct.cur_dir,ct.sort # mandatory for all functions
  new_path = parse_path(path,cur_dir)
  word     = u.weak_pop(new_path) # last word means to be autocompleted
  on       = tags_count_sort(tags_autocomplete(c,new_path),sort) # standart preparation
  return complete_tags_on_prefix(on,word) # completion on word,being a prefix

def complete_tags_on_prefix(on,word):
  def filter_func(el):
    if el[0].startswith(word):
      return True
    return False
  return dict(filter(filter_func,on.items())).keys()

    
@dbind(clist,'^cd (.+)\s$')
def complete_cd_without_word(path,ct):
  # :TESTED: 
  c,cur_dir,sort = ct.c,ct.cur_dir,ct.sort # mandatory for all functions
  new_path = parse_path(path,cur_dir)
  on  = tags_autocomplete(c,new_path)
  return tags_count_sort(on,sort).keys()

@dbind(clist,'^ls ([0-9\*\s]*)\s$')
def complete_ls_without_word(nodes,ct):
  c,cur_dir,sort = ct.c,ct.cur_dir,ct.sort # mandatory for all functions
  numbers       = parse_numbers(nodes)
  on            = tags_get_cur_nodes(c,cur_dir)
  return [str(i) for i in misc_ls_difference_update(range(len(on)), numbers)]

@dbind(clist,'^ls ([0-9\*\s]*[^\s])$')
def complete_ls_with_word(nodes,ct):
  last_number    = str(parse_numbers(nodes).pop())
  return [i for i in comlete_ls_without_word(nodes,ct) if i.startswith(last_number)]


@dbind(clist,'^mv ([0-9\*\s]*)$')
def complete_mv_first_part(nodes,ct):
  if nodes[-1] == ' ':
    return complete_ls_without_word(nodes,ct).append('to')
  return complete_ls_with_word(nodes,ct)    
  
    
@dbind(clist,'^mv ([0-9\*\s]*) to (.+)$')
def complete_mv_second_part(nodes,path,ct):
  c,cur_dir,sort = ct.c,ct.cur_dir,ct.sort # mandatory for all functions

  if not u.weak_get(path,-1) == ' ':
    path = parse_path(path,cur_dir)
    word = u.weak_get(path,-1)
    on   = tag_autocomplete(c,word)
    return tags_count_sort_remove_or_all(c,on,sort,path).keys()
  on = sql_get_all(c)
  return tags_count_sort_remove_or_all(c,on,sort,[]).keys()


## Simple complete stuff
@dbind(clist,'^edit ([0-9\*\s]*[^\s])$')
def complete_edit_no_word(nodes,ct):
  return complete_ls_without_word(nodes,ct)

@dbind(clist,'^edit ([0-9\*\s]*\s)$')
def complete_edit_word(nodes,ct):
  return complete_ls_with_word(nodes,ct)

@dbind(clist,'^edit-as-one ([0-9\*\s]*[^\s])$')
def complete_edit_as_one_no_word(nodes,ct):
  return complete_ls_without_word(nodes,ct)

@dbind(clist,'^edit-as-one ([0-9\*\s]*\s)$')
def complete_edit_as_one_word(nodes,ct):
  return complete_ls_with_word(nodes,ct)

@dbind(clist,'^add-from-buffer (.+)$')
def complete_add_from_buffer(path,ct):
  return complete_mv_second_part(None,path,ct)

@dbind(clist,'^cp ([0-9\*\s]*)$')
def complete_cp_first_part(nodes,ct):
  return complete_mv_first_part(nodes,ct)
    
@dbind(clist,'^cp ([0-9\*\s]*) to (.+)$')
def complete_cp_second_part(nodes,path,ct):
  return complete_mv_second_part(nodes,path,ct)



#######  MAIN COMPLETE SECTION
# import re

# def complete_cd(c,line,cur_dir,sort='by_name'):
#   """
#     command looks like cd .. tag1 tag2 tag3 tagN
#     autocomplete  works based on tags, that exist on nodes in <new_dir> level
#     complete tags based on cur_

#   """
#   line      = parse_strip_line_from_command(line)
#   line,word = parse_complete_prepare_line(line)
#   new_path  = parse_path(line,cur_dir)
#   if word:
#     new_path.append(word+'*')
#     tags_autocomplete(c,new_path),sort).keys()

# def complete_cd_free(c,line,cur_dir,sort="by_name"):
#   """ complete that does not based on cur_dir """
#   line      = parse_strip_line_from_command(line)
#   line,word = parse_complete_prepare_line(line)
#   new_path  = parse_path(line,cur_dir)
#   if word:
#     result = set(tags_count_sort(tag_autocomplete(c,word),sort).keys())
#   return []

# def complete_cd_or_free(c,line,cur_dir,sort='by_name'):
#   """
#     Autocomplete algorythm(with word suggestion):
#       1. Try autocomplete with complete_cd,
#       2. otherwise try to autocomplete cd_free
#   """  
#   result = complete_cd(c,line,cur_dir,sort)
#   if not result:
#     return complete_cd_free(c,line,cur_dir,sort='by_name')
#   return result



# def complete_mv(c,line,cur_dir,sort):
#   """
#       Algorythm:
#       1. In case of <word>
#   1. tries to complete directory dependend
#     2. In case of fail, switches to directory independend completion
#   """
#   line         = parse_strip_line_from_command(line)
#   numbers,tags = parse_cp_mv(line)
#   numbers      = parse_numbers(numbers)
#   if tags:
#     return complete_cd_or_free(c,tags,cur_dir,sort)
#   if numbers:
#     ls_on = sql_get(c,matchee=u.tags_to_string(cur_dir))
#     u.everything_to_str(numbers)
#     complete_ls(c,numbers,)
    

  

  
#   #  line,word = parse_complete_prepare_line(line)
#   if parse_is_word(line):
#     result = tag_tags_autocomplete(c,line)
#     if result:
#       # if context dependend tags found
#       return 
#     else:
#       line,word = parse_complete_prepare_line(line)
#       return tags_count_sort(tag_autocomplete(c,word),sort)
#   else:


# def complete_ls(c,line,on):
#   """
#     on is current_nodes in format [(rowid,tags,node,metadata)]
#   """
#   line      = parse_strip_line_from_command(line)
#   # line now has no command (cp,ls,edit e.t.c)
#   line,word = parse_complete_prepare_line(line)
#   # line is args string, and word is non completed(without space in
#   # the end or None
#   line = parse_numbers(line)
#   # line now is a list of numbers    or []
#   word = parse_numbers(line)
#   # word now is a list of one number or []
#   complete_data = set(range(len(on)))
#   if line:
#     complete_data.difference_update(line)
#   complete_data = [str(i) for i in complete_data]
#   if word:
#     word = str(word[0])
#     return [for i in complete_data if i.startswith(word)]
#   return complete_data
#######  MAIN COMMANDS SECTION

# @dbind(clist,'^edit ([0-9\*\s]*[^\s])$')
# def complete_edit_no_word(nodes,ct):
#   return complete_ls_without_word(nodes,ct)

# @dbind(clist,'^edit ([0-9\*\s]*\s)$')
# def complete_edit_word(nodes,ct):
#   return complete_ls_with_word(nodes,ct)

# @dbind(clist,'^edit-as-one ([0-9\*\s]*[^\s])$')
# def complete_edit_as_one_no_word(nodes,ct):
#   return complete_ls_without_word(nodes,ct)

# @dbind(clist,'^edit-as-one ([0-9\*\s]*\s)$')
# def complete_edit_as_one_word(nodes,ct):
#   return complete_ls_with_word(nodes,ct)

@dbind(colist,'^edit ([0-9\*\s]*\s)$')
def command_edit(c,nodes):
  parse_numbers(nodes)
  
@dbind(colist,'^edit-as-one ([0-9\*\s]*[^\s])$')  
def command_edit_as_one(nodes,ct):
  c,cur_dir,sort = ct.c,ct.cur_dir,ct.sort # mandatory for all functions
  on    = tags_get_cur_nodes(c,cur_dir)  # :TODO: memoize
  nodes = misc_ls_get_nodes(on,nodes)
  # optional
  ct.cur_nodes = nodes
  # end optional
  return misc_ls_show(nodes)

  
@dbind(colist,'^ls ([0-9\*\s]*)$')
def command_ls(nodes,ct):
  c,cur_dir,sort = ct.c,ct.cur_dir,ct.sort # mandatory for all functions
  on    = tags_get_cur_nodes(c,cur_dir)  # :TODO: memoize
  nodes = misc_ls_get_nodes(on,nodes)
  # optional
  ct.cur_nodes = nodes
  # end optional
  return misc_ls_show(nodes)


@dbind(colist,'^cp ([0-9\*\s]*) to (.+)$')    
def command_cp(c,nodes,path):
  # cp means append new path to selected nodes
  new_path   = parse_path(tags,cur_dir)
  nodes      = misc_ls_get_nodes(tags_get_cur_nodes(c,cur_dir),nodes)
  tags_append(nodes,new_path)
  
  
@dbind(colist,'^mv ([0-9\*\s]*) to (.+)$')  
def command_mv(c,nodes,path):
  # :MUST implement UNDO:
  c,cur_dir,sort = ct.c,ct.cur_dir,ct.sort # mandatory for all functions
  new_path   = parse_path(path,cur_dir)
  nodes      = misc_ls_get_nodes(tags_get_cur_nodes(c,cur_dir),nodes)
  tags_append_remove(nodes,cur_dir,new_path)

@dbind(colist,'^add-from-buffer (.+)$')  
def command_add_from_buffer(cur_dir,ct):
  # :TODO: Add <display buffer in cli>
  new_path = parse_path(path,cur_dir)
  data     = from_clip()
  tags_set(c,[[new_path,data]])

@dbind(colist,'^mv ([0-9\*\s]*)$')  
def command_paste_to_buffer(nodes,ct):
  cur_nodes =  misc_ls_get_nodes(get_cur_nodes(cur_dir),nodes)
  u.to_clip(misc_ls_show(cur_nodes))


#######  MISC RELATED SECTION
import sqlite3
def misc_ls_show(on):
  t = """ %s~:::: %s ::::~\n%s """
  result = []
  for k,v in enumerate(on):
    rowid,tags,node,metadata = v
    result.append(t%(k,tags,node))
  return '\n'.join(result)

def misc_ls_get_nodes(on,node_list):
  numbers = parse_numbers(node_list)
  if numbers:
    return [u.weak_get(on,i) for i in numbers]
  return on

def misc_ls_get_nodes_by_numbers(c,node_list,cur_dir):
  on = tags_get_cur_nodes(c,cur_dir)
  return misc_ls_get_nodes(on,node_list)

def misc_ls_difference_update(listA,listB):
  for i in listB:
    el_index = u.weak_index(listA,i)
    if el_index:
      del listA[el_index]
      

def misc_tables_populate(c,count=1000):
  sentence = u.a_bit_of_ipsum()[0]
  for i in range(count):
    tags = u.tags_to_string(sentence())
    sql_set(c,([tags,sentence(),None]))

 
def misc_tables_create(c):
  qtags = """ CREATE VIRTUAL TABLE 
    if NOT EXISTS TAG USING
      fts4(tags, node, metadata, tokenize=simple); """
  c.execute(qtags)
 
def misc_prepare(debug=True,populate=False):
  """
    1. Create new dirs(if needed)
    2. Open connection, create cursor
  """
  if debug == True:
    conn = sqlite3.connect(":memory:")
    c    = conn.cursor()
    misc_tables_create(c)
    if populate:
      misc_tables_populate(c)
    return [conn,c]

  new_program_folder = os.path.join(HOME_DIR,DEFAULT_FOLDER_NAME)
  new_nodes_folder   = os.path.join(new_program_folder,NODES_FOLDER)
  if not os.path.exists(new_program_folder):
    os.makedirs(new_program_folder)
  if not os.path.exists(new_nodes_folder):
    os.makedirs(new_nodes_folder)

  conn = sqlite3.connect(os.path.join(new_program_folder,'db'))
  c    = conn.cursor()
  misc_tables_create(c)
  return [conn,c]


    
   


#######  PARSE RELATED SECTION
def parse_path(command,cur_dir):
  # :TESTED: 
  """
    makes path, relative to cur_dir    
  """
  cur_dir = cur_dir[:] #copy of cur dir
  exp = re.compile("(\.\.)|(\/)|\s")
  for i in filter(lambda x: x, exp.split(command)):
    if i == '..':
      u.weak_pop(cur_dir)
    elif i == '/':
      cur_dir = []
    else:
      cur_dir.append(i)
  return cur_dir

def parse_cp_mv(args):
  """
    parse args like:
       4 5 6 7 to asd bsd csd
    return [[tagsd,asdf,vvv,sdf],[4,5,6,7]]
  """
  # here we split two arrays by <to> keyword
  args = u.sp_split(args)
  
  nodes,tags = u.split_list(args, 'to')
  return [nodes,u.everything_to_str(tags)]

def parse_numbers(targs):
  return u.filter_number(u.everything_to_list(targs))
  
def parse_strip_line_from_command(line):
  pattern = re.compile('cd|ls|cp|mv|edit|edit_as_one|add_from_buffer|rm')
  line = u.sp_split(line)
  if pattern.match(line[0]):
    return line[1:]
  return line
def parse_is_word(line):
  """
    this function will determine if completion should be
      by defined word, or
    It should be working on space
  """
  if u.everything_to_str(line)[-1] == ' ':
    return True
  return False

def parse_complete_prepare_line(line):
  """
    return [line,word] where word is
      prefix to complete or None
      line, is a line, without word prefix
  """  
  line = u.sp_split(line)
  if line[-1] == '':
    return [u.everything_to_str(line[:-1]),None]
  return [u.everything_to_str(line[:-2]),line[-1]]
  
  

######## TAGS RELATED SECTION

def tags_append(c,on,tags):
  append_this_tags = u.tags_to_list(tags)
  def update_func(i):
    rowid,tags,node,metadata = i
    node_tags  = set(u.tags_to_list(tags))
    node_tags.update(append_this_tags)
    tags = u.tags_to_string(node_tags)
    return [tags,None,None]
  sql_update(c,on,update_func)

def tags_set(c,on):
  for i in on:
    sql_set(c,i)

def tags_remove(c,on,tags):
  append_this_tags = u.tags_to_list(tags)
  def update_func(i):
    rowid,tags,node,metadata = i
    node_tags  = set(u.tags_to_list(tags))
    node_tags.difference_update(append_this_tags)
    tags = u.tags_to_string(node_tags)
    return [tags,None,None]
  sql_update(c,on,update_func)

def tags_append_remove(c,on,tags_to_remove,tags_to_append):
  " remove same tags, append new tags"
  tags_to_remove = u.tags_to_list(tags_to_remove)
  tags_to_append = u.tags_to_list(tags_to_append)  
  def update_func(i):
    rowid,tags,node,metadata = i
    node_tags = set(u.tags_to_list(tags))
    node_tags.difference_update(tags_to_remove)
    node_tags.union(tags_to_append)
    tags = u.tags_to_string(node_tags)
    return [tags,None,None]
  return sql_update(c,on,update_func)

def tags_count_sort_remove_or_all(c,on,sort,remove_list=[]):
 # on = tags_count(on)
#  if not on:
#    on = tags_count(sql_get_all(c))
  return tags_count_sort(tags_count_remove(on,remove_list),sort)


def tags_autocomplete(c,tags):
  tags_list = u.tags_to_list(tags)
  tags_str  = u.tags_to_string(tags_list)
  on   = tags_count(sql_get(c,matchee=tags_str))
  if not  on:
    on = tags_count(sql_get_all(c))
  return tags_count_remove(on,tags_list)



def tags_count(on):
  result = {}
  for i in on:
    for k in u.tags_to_list(i[1]):
      try:
        result[k] +=1
      except:
        result[k] = 1
  return result

def tag_autocomplete(c,tag):
  tag = tag.strip()+'*'
  on = sql_get(c,matchee=tag)
  return tags_count(on)

def tag_tags_autocomplete(c,tags):
  tags = u.tags_to_string(tags).strip()+'*'
  on   = sql_get(c,matchee = tags)
  return tags_count(on)


def tags_autocomplete_fuzzy(on,word='',sort="by_name",threshold=0.8):
  """ on here is {name:appearance} struct"""
  if not word:
    return {}
  
  def filter_func(el):
    return u.two_words_difference(el[0],word)>=threshold
  on = filter(filter_func,on)
  
  if sort == "by_threshold":
    def sort_func(el):
      return u.two_words_difference(el[0],word)
    return sorted(on,key=sort_func)
  
  return tags_count_sort(on,sort)

def tags_tree_build(on):
  """
    makes a materalized path tree structure in memory
    return :: list  
  """
  result = set([])
  def reduce_func(a,b):
    # hello from hell INTO: 
    #  hello
    #  hello from 
    #  hello from hell 
    result.add(a)
    return '%s %s'%(a,b)
  for i in on:
    reduce(reduce_func,  u.sp_split(i[1]))
  return sorted(result)

def tags_tree_reduce_level(tree,level):
  def filter_func(el):
    len( u.sp_split(el[0])) < level
  return filter(fitler_func, sequence)

def tags_count_sort(on,sort='by_name'):
  """on   == {tag_name:number_of_occurrences} """
  """sort == by_name | by_length """

  if sort == 'by_name':
    def sort_func(el): return el[0].lower()
  if sort == 'by_length':
    def sort_func(el): return el[1]
    
  return OrderedDict(sorted(on.items(),key=sort_func))

def tags_count_remove(on,list_to_remove):
  """
    :CHANGE ORIGINAL <ON> Param:
    remove keys from list
    on  == {name_tag:appearance_count}
  """
  for i in u.tags_to_list(list_to_remove):
    try:
      del on[i]
    except KeyError:
      pass
  return on

      
def tags_get_cur_nodes(c,cur_dir):
  tags =  u.tags_to_string(cur_dir)
  if cur_dir:
    return sql_get(c,matchee=tags)
  else:
    return sql_get_notags_nodes(c)

def tags_make_cloud(on,sort='by_name'):
  data = tags_count_sort(on,sort)
  return ["%s (%s)"%(k,v) for k,v in data.items()]

######## DATABASE RELATED SECTION
def sql_get(c,rowid=None,matcher='tags',matchee=''):
  if rowid:
    return c.execute(\
      """SELECT rowid,tags,node,metadata FROM TAG WHERE rowid = ?""",(rowid,))
  return c.execute(\
    """SELECT rowid,tags,node,metadata FROM TAG WHERE %s MATCH ?"""\
                   %(matcher),(matchee,))

def sql_get_all(c):
  # :TESTED:
  return c.execute(""" SELECT rowid,tags,node,metadata FROM TAG""")

def sql_set(c,data):
  # :TESTED:
  """ data == [tags,node,metadata] """
  return c.execute(""" INSERT INTO TAG (tags,node,metadata) VALUES (?,?,?)""",data)

def sql_update(c,on,func):
  def map_func(k,v):
    if v:
      return ("%s = ?"%k,v)
  for i in on:
    result = map(map_func,zip(['tags','node','metadata'],func(i)))
    query = ','.join(result.keys())
    data  =  result.values()
    data.append(i[0])
    c.execute("""UPDATE TAG SET %s WHERE rowid = ?"""%query,data)

def sql_update_or_create(c,on,func):
  def map_func(k,v):
    if v:
      return ("%s = ?"%k,v)
  for i in on:
    result = map(map_func,zip(['tags','node','metadata'],func(i)))
    query = ','.join(result.keys())
    data  =  result.values()
    if i[0] == None:
      sql_set(c,i[1:])
    else:
      data.append(i[0])
      c.execute("""UPDATE TAG SET %s WHERE rowid = ?"""%query,data)
  

def sql_delete(c,on):
  for i in on:
    c.execute(""" DELETE FROM TAG WHERE rowid = ? """,[i[0]])
  
def sql_get_notags_nodes(c):
  # :SHOULD TEST:
  return c.execute("""SELECT rowid,tags,node,metadata FROM TAG WHERE tags = '' """)


######## FILE RELATED SECTION     
import uuid
import os
import re

def file_parse_file_data(data):
  # :TESTED:
  """
    This function only manages file parsing
    This function does not manage IO,
    For IO data use file_load_data_from_disk instead
    For Updating data to database, use file_update_database
  """
  pattern = u.stp(FROM_DISK_PARSE_PATTERN)
  pattern = re.compile(pattern,re.DOTALL)
  for i in pattern.finditer(data):
    yield i.groupdict()
    
def file_connect_parser_loader(on):
  """
    Takes data from parser, and makes It
    usable by loader
  """
  def map_func(data):
    r = []
    r.append(u.weak_get(data,'rowid'))
    r.append(u.weak_get(data,'tags' ))
    r.append(u.weak_get(data,'node' ))  
    r.append(u.weak_get(data,'metadata'))
    return r
  for i in on:
    yield map_func(i)
   
def file_load_data_from_disk(fname):
  path = os.path.join(PROGRAM_FOLDER,NODES_FOLDER,fname)
  with open(path,'r') as data:
    d =  data.read()
  return d

def file_update_database(c,on):
  def update_func(i):
    rowid,tags,node,metadata = i
    tags = u.tags_to_string(tags)
    return [tags,node,metadata]
  return sql_update_or_create(c,on,update_func)

def file_update_from_file(c,file_name):
  # :Main func:
  data          = file_load_data_from_disk(file_name)
  parsed_data   = file_parse_file_data(data)
  prepared_data = file_connect_parser_loader(parsed_data)
  return file_update_database(c,prepared_data)

def file_generate_unique_file_name_in_path():
  filename = str(uuid.uuid4())
  return os.path.join(HOME_DIR,NODES_FOLDER,filename)



def file_flush_to_disk(data,as_one=False):
  """
    data = (rowid,tags,node,metadata)
  """
  def map_func(i):
    rowid,tags,node,metadata = i
    return TO_DISK_FLUSH_PATTERN.\
      format(rowid=rowid,tags=tags,node=node,metadata=metadata)
  
  def map_func_as_one(i):
    with open(file_generate_unique_file_name_in_path(),'w') as new_file:
      new_file.write(map_func(i))
      
  if as_one:
    with open(name,'w') as new_file:
      new_file.write('\n'.join(map(map_func,on)))
  else:
    map(map_func_as_one,data)
  
def file_open_in_editor(paths=[]):
  for i in paths:
    os.popen("%s %s"(DEFAULT_EDITOR,i)) 
  
def file_clean(self,delta=4):
  """
    remove all edit files with delta (in days) more than <delta value> 
  """
  def solver(datetime):
    """
      if True,  delete file
      if False, save   file
    """
    delta_from_now_in_days = (datetime.datetime.now() - datetime).days
    if delta_from_now_in_days > delta:
      return True
    return False

  for i in os.listdir(os.path.join(PROGRAM_FOLDER,NODES_FOLDER)):
    path = os.path.join(PROGRAM_FOLDER,NODES_FOLDER,i)
    this_file_datetime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    if solver(this_file_datetime):
      os.remove(path)

# END FILE RELATED SECTION




def constructor(func,*default_args):
  def result_function(*function_args):
    result = list(function_args)
    result.extend(default_args)
    result = tuple(result)
    return func(*result)
  
  return result_function




###### MISC COMMANDS
