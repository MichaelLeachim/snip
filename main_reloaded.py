import utils as u
######## COMPLETE RELATED SECTION ##########

def complete_cd(c,path,sort='by_name',with_word=False):
  # TESTED 
  if with_word:
    word = u.weak_pop(path)
  if not path:
    on = sql_get_all(c)
  else:
    str_path = ' '.join(sorted(set(path)))
    on = sql_get(c,matchee=str_path)
    
  on = tags_count_sort(tags_count(on),sort)
  if not on:
    return []
  result = (k for k,v in on  if not (k in path))
  if with_word:
    return (i for i in result if i.startswith(word))
  
  return (i for i in result if i)


def complete_ls(c,nodes,cur_dir,with_word=False):
  on = (str(i) for i in range(len(list(dir_nodes(c,cur_dir)))) if not (i in nodes))

  if with_word:
    word = str(u.weak_pop(nodes))
    return (i for i in on if i.startswith(word))
  return u.generator_append(['*'],on)
  
def dir_nodes(c,path):
  path = ' '.join(set(path))
  data = sql_get(c,matchee=path)
  data = u.generator_is_not_empty(data)
  if not data:
    return sql_get_all(c)
  return data

#complete_mv(c,nodes=[1,2],cur_dir = [],path=['python','example','quicksort'],    with_word=False,sort=sort)
def complete_mv(c,nodes,cur_dir,path,with_word,sort):
  if (not path):
    return complete_ls(c,nodes,cur_dir,with_word)

  data  = tags_count_sort(tags_count(sql_get_all(c)),sort)
  data  = u.list_minus_list((i[0] for i in data if i),path)
  if with_word:
    word = u.weak_pop(path)
    return (i for i in data if i.startswith(word))
    
  return data  
  
  


def misc_tables_create(c):
  #: TANGENT TESTED : 
  qtags = """ CREATE VIRTUAL TABLE 
    if NOT EXISTS TAG USING
      fts4(tags, node, metadata, tokenize=simple); """
  c.execute(qtags)

  

####### TAGS RELATED SECTION


def tags_count(on):
  #: TANGENT TESTED : 
  result = {}
  for i in on:
    for k in u.tags_to_list(i[1]):
      try:
        result[k] +=1
      except:
        result[k] = 1
  return result

def tags_count_sort(on,sort='by_name'):
  #: TANGENT TESTED
  """on   == {tag_name:number_of_occurrences} """
  """sort == by_name | by_length """

  if sort == 'by_name':
    def sort_func(el): return el[0].lower()
  if sort == 'by_length':
    def sort_func(el): return el[1]
    
  return sorted(on.items(),key=sort_func)


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
  return c.executemany(""" INSERT INTO TAG (tags,node,metadata) VALUES (?,?,?)""",data)

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

    
