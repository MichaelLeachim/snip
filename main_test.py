#!encoding: utf-8
import utils as u
from static import *
import main_reloaded as m
import re
#from  utils_for_test import db_prepare
import pytest
import sqlite3
#conn,c = m.misc_prepare()

# set_data = [[u"python django view testing", u'node_data',u'metadata'],
#             [u"python quicksort ruby",      u'node_data',u'metadata'],
#             [u"ruby rails controller example ",    None,u'metadata']]
set_data = [[u"django python testing view",     u'node_data',u'metadata'],
            [u"python quicksort  ruby",         u'node_data',u'metadata'],
            [u"controller example rails ruby",  None,u'metadata']]

# operated_data = [(1,u"python django view testing",  u'node_data',u'metadata'),
#                  (2,u"python quicksort ruby",       u'node_data',u'metadata'),
#                  (3,u"ruby rails controller example ",    None,u'metadata')]
operated_data = [ (1,u"django python testing view",     u'node_data',u'metadata'),
                  (2,u"python quicksort  ruby",         u'node_data',u'metadata'),
                  (3,u"controller example rails ruby",  None,u'metadata')]

tags_count_data = {"python":2, \
  "django":1, 
  "view":1, 
  "testing":1,
  "quicksort":1,
  "ruby": 2,
  "rails":1,
  "controller":1,
  "example":1}
#print tags_count_data

@pytest.fixture
def cconn():
  conn = sqlite3.connect(":memory:")
  c    = conn.cursor()
  m.misc_tables_create(c)
  m.sql_set(c,set_data)
  def fin():
    print ("finalizing %s (%s)" % (conn,c))
    conn.close()
  return [conn,c]

def test_cconn(cconn):
  conn,c = cconn
  assert list(m.sql_get_all(c)) == operated_data

def test_sql_update(cconn):
  conn,c = cconn

  _operated_data = [ (1,u"dalalay",  u'3333',   u'metadata'),
                     (2,u"dalada",   u'222',    u'metadata'),
                     (3,u"dibuday",  u'tratata',u'metadata'),
                     (None,u"asd",  u'dsd',None)]
  new_operated_data = [(1,u"dalalay",  u'3333',   u'metadata'),
                       (2,u"dalada",   u'222',    u'metadata'),
                       (3,u"dibuday",  u'tratata',u'metadata'),
                       (4,u"asd",  u'dsd',None)]
  m.sql_update(c,_operated_data)
  assert list(m.sql_get_all(c)) == new_operated_data

  
  

def test_complete_cd(cconn):
  conn,c = cconn
  
  path = ["python"]
  sort = "by_name"
  assert list(m.complete_cd(c,path,sort='by_name',with_word=False)) == sorted(['django','view','testing','quicksort','ruby'])

  path = ['python','ruby']
  assert list(m.complete_cd(c,path,sort,with_word=False)) == ['quicksort']

  path = []
  assert len(list(m.complete_cd(c,path,sort))) == len(tags_count_data)

  path = ['r']
  assert list(m.complete_cd(c,path,sort,with_word=True)) == ['rails','ruby']

  path = ['python','r']
  assert list(m.complete_cd(c,path,sort,with_word=True)) == ['ruby']

  path = ['zrobodon']
  assert list(m.complete_cd(c,path,sort,with_word=True)) == []



def test_dir_nodes(cconn):
  conn,c = cconn
  path   = ['python']
  assert list(m.dir_nodes(c,path)) == operated_data[:2]

  path   = []
  assert list(m.dir_nodes(c,path)) == operated_data


def test_complete_ls(cconn):
  conn,c = cconn
  m.sql_set(c,set_data)
  m.sql_set(c,set_data)
  m.sql_set(c,set_data)
  
  cur_dir = []
  nodes   = [0,1,3]
  assert list(m.complete_ls(c,nodes,cur_dir,with_word=False))  == ['*','2','4','5','6','7','8','9','10','11']
  
  nodes   = [1]
  assert list(m.complete_ls(c,nodes,cur_dir,with_word=True))   == ['1','10','11']

  nodes = ['*']
  assert list(m.complete_ls(c,nodes,cur_dir,with_word=True))   == []

  nodes = []
  assert list(m.complete_ls(c,nodes,cur_dir,with_word=True))   == []

  nodes = []
  assert list(m.complete_ls(c,nodes,cur_dir,with_word=False))  == ['*','0','1','2','3','4','5','6','7','8','9','10','11']

  nodes = ['fuck']
  assert list(m.complete_ls(c,nodes,cur_dir,with_word=True))   == []
  
def test_tags_count(cconn):
  conn,c = cconn
  assert sorted(m.tags_count(m.sql_get_all(c)).keys()) == sorted(tags_count_data.keys())


def test_tags_to_list():
  tags = 'asd  bsd dsd csd  bsd    asd '
  assert u.tags_to_list(tags) == ['asd','bsd','csd','dsd']
  tags = set(['z','a'])
  assert u.tags_to_list(tags) == ['a','z']

def test_tags_to_str():
  tags = 'asd  bsd dsd csd  bsd    asd '
  assert u.tags_to_str(tags) == "asd bsd csd dsd"
  tags = set(['z','a'])
  assert u.tags_to_str(tags) == "a z"
  assert u.tags_to_str("django python-2.7 web-programming testing view") == 'django python-2.7 testing view web-programming'
  assert u.tags_to_str(set(["django","python-2.7", "web-programming", "testing", "view"])) == 'django python-2.7 testing view web-programming'
  

def test_tags_count_sort(cconn):
  conn,c = cconn
  data   = m.tags_count(m.sql_get_all(c))
  data = [i[0] for i in m.tags_count_sort(data,'by_name')]
  assert data == sorted(tags_count_data.keys())

def test_complete_mv(cconn):
  conn,c = cconn
  with_word = True
  sort      = "by_name"
  local_tags_count_data = list(sorted(tags_count_data.keys()[:]))
  assert list(m.complete_mv(c,nodes=[], cur_dir=[],path=[],with_word=False,sort=sort))  == ['*','0','1','2']
  # mv cd algorythm: (just show all possible completions)
  # alternative: (show matched first,in case of not_found, match from everything else)
  # path is already compiled path from <input_line> and <
  local_tags_count_data.remove('python')
  local_tags_count_data.remove('example')
  local_tags_count_data.remove('quicksort')  
  assert list(m.complete_mv(c,nodes=[1,2],cur_dir=[],path=['python','example','quicksort'],    with_word=False,sort=sort)) ==  local_tags_count_data
  assert list(m.complete_mv(c,nodes=[1,2],cur_dir=[],path=['python','example','quicksort','r'],with_word=True, sort=sort)) ==  ['rails','ruby']
  #assert list(m.complete_mv(c,nodes=[1,2],cur_dir=[],path=['python','example','quicksort','r'],with_word=False,sort=sort)) ==  [] it is not right
  assert list(m.complete_mv(c,nodes=[1,2],cur_dir=[],path=[],                                  with_word=False,sort=sort)) ==  ['*','0']
  assert list(m.complete_mv(c,nodes=[],   cur_dir=[],path=[],                                  with_word=False,sort=sort)) ==  ['*'] + [str(i) for i in range(len(operated_data))]

  
def test_split_list():
  x = ['hello','from','hell']
  assert u.split_list(x,'from')  == [['hello'],['hell']]
  assert u.split_list(x,'hello') == [[],['from','hell']]  
  assert u.split_list(x,'hell')  == [['hello','from'],[]]

def test_list_minus_list():
  list(u.list_minus_list(range(1,5),range(3,8))) == [1,2,3]

def test_generator_is_not_empty():
  # test utils
  x = (i for i in range(1,10))
  assert list(u.generator_is_not_empty(x)) == range(1,10)

  x = (i for i in range(1,2))
  x.next()
  assert u.generator_is_not_empty(x) == False

def test_command_mv(cconn):
  # [python] mv 1 2 .. python2.7

  # []       mv * proging-stuff

  _operated_data = [(1,u"django python testing view",     u'node_data',u'metadata'),
                    (2,u"python quicksort  ruby",         u'node_data',u'metadata'),
                    (3,u"controller example rails ruby",  None,u'metadata')]
  c,conn = cconn
  nodes     = ['*']
  cur_dir   = ['python']
  new_path  = ['python-2.7 web-programming']
  _new_operated_data = [(1,u"django python-2.7 testing view web-programming",u'node_data',u'metadata'),
                        (2,u"python-2.7 quicksort ruby web-programming",   u'node_data',u'metadata'),
                        (3,u"controller example rails ruby",                 None,        u'metadata')]
  m.command_mv(c,nodes,cur_dir,new_path)
  assert list(m.sql_get_all(c)) == _new_operated_data


def test_command_mv_2(cconn):
  #======================
  c,conn = cconn
  print list(m.sql_get_all(c))
  nodes     = [0]
  cur_dir   = ['python']
  new_path  = ['python-2.7']
  _new_operated_data = [(1,u"django python-2.7 testing view",     u'node_data',u'metadata'),
                        (2,u"python quicksort  ruby",         u'node_data',u'metadata'),
                        (3,u"controller example rails ruby",  None,u'metadata')]
  m.command_mv(c,nodes,cur_dir,new_path)
  assert list(m.sql_get_all(c)) == _new_operated_data
  #======================

def test_command_ls(cconn):
  operated_data = [ (1,u"django python testing view",     u'node_data',u'metadata'),
                    (2,u"python quicksort  ruby",         u'node_data',u'metadata'),
                    (3,u"controller example rails ruby",  None,u'metadata')]
  c,conn = cconn
  cur_dir = ['python']
  return_data = """0 ID:1 TAGS: django python testing view
node_data
==============================
1 ID:2 TAGS: python quicksort ruby
node_data
==============================""" # amazing, I did not know it
  assert m.command_ls(c,cur_dir) == return_data

def test_complete_new(cconn):
  c,conn = cconn
  path = ['python','django','quicksort','testing','view','ruby','example']
  assert list(m.complete_new(c,path,with_word=False)) == ['controller','rails']
  path.append('ra')
  assert list(m.complete_new(c,path,with_word=True)) == ['rails']

def test_command_new(cconn):
  c,conn = cconn
  _operated_data = [(1,u"django python testing view",     u'node_data',u'metadata'),
                    (2,u"python quicksort  ruby",         u'node_data',u'metadata'),
                    (3,u"controller example rails ruby",  None,u'metadata'),
                    (4,u"azorgos django memoris python",  u'afaik',None)]
  
  m.command_new(c,tags=['python','django','azorgos','memoris'],node_data='afaik',metadata=None)
  assert list(m.sql_get_all(c)) == _operated_data

def test_command_cp(cconn):
  c,conn = cconn
  cur_dir = ['python','django']
  nodes   = ['*']
  new_dir = ['azog','micklagazos']
  _newly_operated_data = [(4,u"azog micklagazos testing view",     u'node_data',u'metadata')]
  m.command_cp(c,nodes,cur_dir,new_dir)
  assert list(m.sql_get(c,rowid=4)) == _newly_operated_data
  
def test_command_cp2(cconn):
  c,conn = cconn
  nodes = ['*']
  cur_dir = []
  new_dir = ['AAA']
  _newly_operated_data = [(4,u"AAA django python testing view",     u'node_data',u'metadata'),
                          (5,u"AAA python quicksort ruby",         u'node_data',u'metadata'),
                          (6,u"AAA controller example rails ruby",  None,u'metadata')]
  operated_data.extend(_newly_operated_data)
  m.command_cp(c,nodes,cur_dir,new_dir)
  assert list(m.sql_get_all(c)) == operated_data

  
 
def test_nodes_by_number(cconn):
  c,conn = cconn
  cur_dir = ['python']
  nodes = ['*']
  assert  list(m.nodes_by_number(c,['python'],['*']))  == operated_data[:2]
  assert  list(m.nodes_by_number(c,['python'],[0]))    == operated_data[:1]
  assert  list(m.nodes_by_number(c,['example'],[0]))   == [operated_data[2]]
  assert  list(m.nodes_by_number(c,[],[0]))    == [operated_data[0]]
  assert  list(m.nodes_by_number(c,[],[112]))  == []
 
      
       
  
  
    
def test_another_mv(cconn):
  #:SHOULD IMPLEMENT:
  # [python] mv quicksort quicksort-old
  # [python] mv 
  # mv python python2-7 
  # mv rails  RoR
  c,conn = cconn
  pass



  
  



  
  
  
  




# def test_tags_count():
#   assert m.tags_count(operated_data) == tags_count_data
  
# def test_tags_count_sort():
#   m.tags_count_sort(tags_count_data,'by_name')[0][0]   == 'django'
#   m.tags_count_sort(tags_count_data,'by_length')[0][0] == "python"
  
  

  

  
# # метро пролетарская 
# # последний вагон
# # дом из красного кирпича
# # дом 11 кв 288 5 подъезд 11 этаж
# # 10 суббота   

# def test_parse_path():
#   path = '.. hello from hell'
#   cur_dir = ['hell','asd','bsd']
#   assert m.parse_path(path,cur_dir) == ['hell','asd','hello','from','hell']

#   path    = '.. .. hello / hell'
#   cur_dir = []
#   assert m.parse_path(path,cur_dir) == ['hell']

# # #def test_dispatcher()

# # #def test_cd
# # #  ct.cur_dir 
# # # def test_cd_complete

# # # def test_mv
# # # def test_mv_complete

# # # def test_edit
# # # def test_edit_as_one

# # # def test_cp
# # # def test_cp_complete




  


  
    

  
