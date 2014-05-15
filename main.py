
#######  MAIN COMPLETE SECTION
import re

 

def complete_cd(c,line,cur_dir,sort='by_name'):
  """
    command looks like cd .. tag1 tag2 tag3 tagN
    autocomplete  works based on tags, that exist on nodes in <new_dir> level
    complete tags based on cur_dir 
  """
  line      = parse_strip_line_from_command(line)
  line,word = parse_complete_prepare_line(line)
  new_path  = parse_path(line,cur_dir)
  if word:
    new_path.append(word+'*')
  return tags_count_sort(tags_autocomplete(c,new_path),sort).keys()

def complete_cd_free(c,line,cur_dir,sort="by_name"):
  """ complete that does not based on cur_dir """
  line      = parse_strip_line_from_command(line)
  line,word = parse_complete_prepare_line(line)
  new_path  = parse_path(line,cur_dir)
  if word:
    result = set(tags_count_sort(tag_autocomplete(c,word),sort).keys())
    
    
  return []

def complete_cd_or_free(c,line,cur_dir,sort='by_name'):
  """
    Autocomplete algorythm(with word suggestion)
    Try autocomplete with complete_cd,
    otherwise try to autocomplete cd_free
  """  
  result = complete_cd(c,line,cur_dir,sort)
  if not result:
    return complete_cd_free(c,line,cur_dir,sort='by_name')
  return result

def complete_mv(c,line,cur_dir,sort):
  """
  mv completion
    Algorythm:
      1. In case of <word>
  1. tries to complete directory dependend
    2. In case of fail, switches to directory independend completion
  """
  line      = parse_strip_line_from_command(line)
  #  line,word = parse_complete_prepare_line(line)
  if parse_is_word(line):
    result = tag_tags_autocomplete(c,line)
    if result:
      # if context dependend tags found
      return 
    else:
      line,word = parse_complete_prepare_line(line)
      return tags_count_sort(tag_autocomplete(c,word),sort)
  else:

    
    
    
  
    

def complete_ls(c,line,on):
  """
    on is current_nodes in format [(rowid,tags,node,metadata)]
  """
  line      = parse_strip_line_from_command(line)
  # line now has no command (cp,ls,edit e.t.c)
  line,word = parse_complete_prepare_line(line)
  # line is args string, and word is non completed(without space in
  # the end or None
  line = parse_numbers(line)
  # line now is a list of numbers    or []
  word = parse_numbers(line)
  # word now is a list of one number or []
  complete_data = set(range(len(on)))
  if line:
    complete_data.difference_update(line)
  complete_data = [str(i) for i in complete_data]
  if word:
    word = str(word[0])
    return [for i in complete_data if i.startswith(word)]
  return complete_data

#######  MAIN COMMANDS SECTION
def command_cd(c,targs):
  
  
  
def command_ls(c,targs):

def command_edit(c,targs):
def command_edit_as_one(c,targs):


  
def command_cp(c,targs):
  nodes,tags = parse_cp_mv(targs)
  
def command_mv(c,targs,cur_dir):
  nodes,tags = parse_cp_mv(targs)
  new_path   = parse_path(tags,cur_dir)
  tags_remove()
  
  
  
  
  
  

def command_add_from_buffer(c,targs)

def command_rm(c,targs):


  
  
  


#######  MISC RELATED SECTION
import sqlite3
def misc_ls_show(on):
  t = """ %s~:::: %s ::::~\n%s """
  result = []
  for k,v in enumerate(on):
    rowid,tags,node,metadata = v
    result.append(t%(k,tags,node))
  return '\n'.join(result)

def misc_ls_get_nodes(on):
  node_numbers = misc_parse_numbers(on)
  on = list(on)
  if node_numbers:
    return [u.weak_get(on,i) for i in node_numbers]
  return on

def misc_complete_exclude_visited(comparison_getter,list_to_complete,list_to_exclude):
  def filter_func(el):
    if comparison_getter(el) in list_to_exclude:
      return False
    return True
  filter(filter_func,list_to_complete)
    


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
 
def misc_prepare(debug=True):
  """
    1. Create new dirs(if needed)
    2. Open connection, create cursor
  """
  if debug == True:
    conn = sqlite3.connect(":memory:")
    c    = conn.cursor()
    misc_tables_create(c)
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
  for i in filter(lambda x: x, exp.split(arg)):
    if i == '..':
      u.weak_pop(cur_dir)
    if i == '/':
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
    tags,node,metadata = i
    node_tags  = set(u.tags_to_list(tags))
    node_tags.update(append_this_tags)
    tags = u.tags_to_string(node_tags)
    return [tags,None,None]
  sql_update(c,on,update_func)

def tags_remove(c,on,tags):
  append_this_tags = u.tags_to_list(tags)
  def update_func(i):
    tags,node,metadata = i
    node_tags  = set(u.tags_to_list(tags))
    node_tags.difference_update(append_this_tags)
    tags = u.tags_to_string(node_tags)
    return [tags,None,None]
  sql_update(c,on,update_func)

    

def tags_autocomplete(c,tags):
  tags = u.tags_to_string(tags)
  on   = sql_get(c,matchee=tags)
  return tags_count(on)

def tags_count(on)
  result = {}
  for i in on:
    for k in u.tags_to_list(i[0]):
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
    return sorted(on,sort_func)
  
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
    def sort_func(el): return el[0]
  if sort == 'by_length':
    def sort_func(el): return el[1]
  return dict(sorted(tags_count(on).items(),sort_func))

def tags_count_difference_update(on,diff_list):
  """
    acts like set.difference_update on tags_count data
      struct {name:count}
    returns the same struct
  """
  def filter_func(el):
    if el[0] in diff_set:
      return False
    return True
  return dict(filter(filter_func,on.items()))
      
  
  
  
  

def tags_make_cloud(on,sort='by_name'):
  data = tags_count_sort(on,sort)
  return ["%s (%s)"%(k,v) for k,v in data] 

  
  
    
    
    





######## DATABASE RELATED SECTION

def sql_get(c,rowid=None,matcher='tags',meatchee=''):
  if rowid:
    return c.execute(\
      """SELECT rowid,tags,node,metadata FROM TAG WHERE rowid = ?""",(rowid,))
  return c.execute(\
    """SELECT rowid,tags,node,metadata FROM TAG WHERE ? MATCH ?""",(matcher,matchee))

def sql_set(c,data):
  """ data == [tags,node,metadata] """
  return c.execute(""" INSERT INTO TAG (tags,node,metadata) VALUES (?,?,?)""",(data,))


def sql_update(c,on,func):
  """On is a list, or a query, where
  each element is [rowid,tags,node,metadata]
  """
  for i in on:
    part_q = []
    data   = []
    for k,v in zip(['tags','node','metadata'],func(i)):
      if v:
        result.append("%s = ?"%k)
        part_q.append(v)
        
    part_q  = ','.join(partq)
    data.append(i[0])
  
    c.execute("""UPDATE TAG SET %s WHERE rowid = ? """%part_q,data)

def sql_delete(c,on):
  for i in on:
    c.execute(""" DELETE FROM TAG WHERE rowid = ? """,[i[0]])
  
  

  



######## FILE RELATED SECTION     
import uuid
import os
import re


def parse_from_disk(data):
  """
    data is like this:
      ~:::: ID-12345 tag1 tag2 tag3 ::::~    
      klfs xcvl sdf xcvl sfd 
      ~:::: tag2 tagdsf xclvx cvsdf sdf xcv ::::~
  """

  splitter = re.compile('(~::::.*?::::~)|(.*?)',re.DOTALL)
  tags     = re.compile('^~::::(.*?)::::~$',re.DOTALL)
  rowid    = re.compile('ID-[0-9]+?\s')
  result = []
  cur_tags = ''

  def get_from_tag_string(pattern,tag_string):
    """ return [Retrieved_Element, tag_string_without_retrieved_element] """
    if not tag_string:
      return ['','']
    result = list(pattern.findall(tag_string))
    if result:
      return [result[0],pattern.sub('',tag_string)]
    return [None,tag_string]


  for i in splitter.split(data):
    if not (i == None) and  not (i == ''):        
      if tags.match(i):
        cur_tags  = tags.findall(i)[0]
      else:
        __rowid,cur_tags = get_from_tag_string(rowid, cur_tags)
        __rowid          = get_from_tag_string(re.compile("[0-9]+"), __rowid)[0] 

        result.append([__rowid,cur_tags,i])
        cur_tags = ''
  return result  


def generate_unique_file_name_in_path():
#  name = str(datetime.datetime.now())
  filename = str(uuid.uuid4())
  return os.path.join(HOME_DIR,NODES_FOLDER,filename)
  #now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d-%H:%M:%S")
  

def from_files_to_database(path):
  with open(path,'r') as node:
    result = parse_from_disk(node.read())

  for rowid,tags,node_data in result:
    if rowid == None:
      new_node(c, tags, node_data)
    else:
      replace_or_do_not_touch(c,rowid,tags,node_data)



def flush_to_disk(data,as_one=False):
  """
    data = [
      (rowid,tags,node_data)
    ]
  """
  paths_that_will_be_returned = []
  result = []

  for i in data:
    result.append("""~:::: ID-%s %s ::::~ \n %s\n"""%(i[0],i[1],i[2]))

  if as_one:
    name = generate_unique_file_name_in_path()
    with open(name,'w') as new_file:
      new_file.write('\n'.join(result))
    return [name]
  else:
    for i in  result:
      name = generate_unique_file_name_in_path()
      with open(name,'w') as new_file:
        new_file.write(i)
        paths_that_will_be_returned.append(name)

  return paths_that_will_be_returned




def open_in_editor(paths=[]):
  for i in paths:
    os.popen("%s %s"(DEFAULT_EDITOR,i)) 
  
  
def clean(self,delta=4):
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
