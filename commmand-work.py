mv 7 6 2 3 4 to asdf vghd norot


^mv ([0-9\*\s]*) to (.*?)$,autocomplete_mv(numbers,tags)


^mv ([0-9\*\s]*) to (.*?)$,autocomplete_mv(numbers,tags)

^mv ([0-9\*\s]*)$          autocomplete_ls(numbers)



^ls ([0-9\*\s]*) complete_ls(numbers)


^cd (.*?) $
^cd (.*?)$

def bind(func_list,regexp,function):
  if type(regexp) == str:
    regexp = re.compile(regexp)
  datastruct= (regexp,function)
  func_list.append(datastruct)
  return func_list

def worker(line,func_list,*params):
  """Worker finds suitable function from func list
     It passes result from parsing to this list, 
     and  appends arguments from params to it
  """
  params = list(params)
  for k,v in func_list:
    if k.match(line):
      data = k.findall(line)
      data.extend(params)
      return v(*data)


def hello(*args,**kwargs):
  print kwargs['c']

hello(c='Zoidberg')


      
"^mv ([0-9\*\s]*) to (.+)$" complete_cd_free(nodes,tags)
"^mv ([0-9\*\s]*)$"        complete_ls(nodes)
#"^mv ([0-9\*\s]*)[0-9]$" complete_ls_with_number
"^cd (.+)$"       complete_cd
"^edit-as-one ([0-9\s\*]*)$"  edit_as_one(nodes)





def complete_mv(nodes):
  

def complete_mv(nodes,tags):
  parse_is_word(tags)
  


x = re.compile('^mv ([0-9\*\s]*) to (.*?)$')
x = re.compile("((f)(u)(c)(k))")
print x.findall('fuck')[0][2]

  





















  

