###
#
#
#
###
# cd python dj`kstra
# cd djkstra
# cd root

# cloud
# tree
# ls
# =====1======tag1 tag2 tag3 tagN===========================
# asdj zxc sadasd zcx
# =====2======tag1 tag2 python ogogo =======================
# new-from-cliboard <enter> tag1,tag2,tag3,
# TODO: new-symlink
# TODO: new-hardlink
# =====3==================================
# to-clipboard (numbers of elements)

# add-tags    aliases 1,2,3,4,5 tag1 tag2 tag3 tagN
# change-tags aliases 1,2,5     tag1 tag3 tagN
# chroot      ~/   --change working directory.
#
# mv 1 3 5 6 7 /
#
#
#
import cmd
import utils as u
from static import *
import main as m
import re

conn,c = m.misc_prepare()
#cmd.Cmd



ct = m.manage_ContextObject()
ct.c = c
ct.sort= 'by_name'
ct.cur_nodes = []
ct.cur_dir   = []
class View(cmd.Cmd):
  prompt = '>'
  # def __init__(self,c,cur_dir=[],sort='by_name'):
  #   self.ct = m.manage_ContextObject()
  #   self.ct.c         = c
  #   self.ct.cur_dir   = cur_dir
  #   self.ct.sort      = 'by_name'
  #   self.ct.cur_nodes = []
#    super(View,self).__init__()
    
  def completedefault(self,text,line, begidx, endidx):
    self.line = line
    return  m.manage_worker(line,m.clist,ct)
  def default(self,line):
    print m.manage_worker(line,m.colist,ct)

  
    
  def do_line(self,line):
    print self.line

#  def help_cd(self):
#    print 'some help on cd'

  def do_bye(self):
    print 'agr'
    return True
print list(m.sql_get_all(c))
r_m = lambda: reload(m)
v = View()
v.cmdloop()


    

#import sys  
#nsys.stdout.write()
#sys.stdin.readline()
  

  
    
    


#nTODO: write view
#  Test view





# class View(cmd.Cmd):
#   #def __init__(self,*args,**kwargs):
#   intro     = 'Welcome to hell!'
#   cur_dir   = []
#   cur_nodes = []
#   prompt    = '>'
#   #  super(View, self).__init__(*args,**kwargs)

#   #identchars = '(0)'
#   #ruler = "="

#   def do_ls(self,args):
#     nodes = self.get_nodes_by_numbers(args)
#     view_nodes(nodes)

#   def complete_ls(self,text,line,*args):
#     line = strip_line_from_command(line)
#     if text:
#       return [str(i) for i in range(len(self.cur_nodes))\
#               if str(i).startswith(str(text))]
#     else:
#       return [str(i) for i in range(len(self.cur_nodes))]
#   def help_ls(self):
#     """
#       ls shows nodes in format
#       ~ 1 :::: Tag1 Tag2 Tag3 TagN :::: ~
#       node content
#       ~ 2 :::: Tag2 Tag3 Tag4 TagN :::: ~
#       node content

#       By calling ls 1 3 5, You will have nodes under number
#       1 3 5 displayed.
#       By calling ls, You will have all nodes displayed.
#     """

#   # COMMAND EDIT =======================================

#   def do_edit_as_one(self,args):
#     nodes = self.get_nodes_by_numbers(args)
#     paths = main.flush_to_disk(nodes,as_one=True)
#     main.open_in_editor(paths)

#   def complete_edit_as_one(self,text,line,*args):
#     return self.complete_ls(text, line)

#   def do_edit(self,args):
#     nodes = self.get_nodes_by_numbers(args)
#     paths = main.flush_to_disk(nodes,as_one=False)
#     main.open_in_editor(paths)

#   def complete_edit(self,text,line,*args):
#     return self.complete_ls(text, line)

# #  def system_cd_autocomplete(self,args):
# #    splitter = re.compile('(\.\.)|(\.)|(\/)|(\/\/)|(~)')
# #    path     = HOME_DIR.split('/')
# #    new_path = args.split('/')
# #    for i in new_path:
#   def complete_cp_mv(self,text,line):
#     line = strip_line_from_command(line)
#     nodes,tags   = cp_mv_args_parse(line)


#     u.sp_split(args)

#   def do_cp(self,args):
#     """
#       syntax:  cp 3 4 5 6 to / hello from hell
#     """
#     tags,nodes = cp_mv_args_parse(args)
#     nodes      = self.get_nodes_by_numbers(' '.join(nodes))
#     tags       = ' '.join(tags)
#     for node in nodes:
#       main.new_node(c, tags, node)

#   def complete_cp(self,text,line,*args):
#     line = strip_line_from_command(line)
#     nodes,tags = cp_mv_args_parse(line)

#     if not line:
#       return self.complete_ls(text, line)

#   def complete_cp_mv(self,text,line):
#     # SPLIT in nodes, tags
#     # IF no tags, complete nodes
#     # ELSE complete tags, context sensitive
#     # otherwise complete tags context insensitive



#   def do_mv(self,args):
#     """
#       syntax:  mv 3 4 5 6 to hello from hell
#     """

#     tags,nodes = self.cp_mv_args_parse(args)
#     if not nodes:
#       print "Nothing selected"
#       break
#     if not tags:
#       print """ You must specify new tags """
#       break

#     main.replace_or_do_not_touch(


#   def complete_mv(self,text,line,*args):
#     # context free completion.
    
#     line = self.strip_line_from_command(line)
#     tags,nodes = self.cp_mv_args_parse(line)
    
#     if not tags:
#       return self.complete_ls(text, line)


#   #===================  CD COMMAND ======================================

#   def do_cd(self,args):
#     self.cur_dir = self.prepare_cd(args, self.cur_dir)
#     self.prompt = '>' + '/'.join(self.cur_dir)



#   def complete_cd(self,text,line,*args):
#     line = self.strip_line_from_command(line)
#     self.prepare_cd(line,self.cur_dir)



#     line = ' '.join(self.prepare_cd(line,self.cur_dir))
#     return ["%s (%s)"%(v,k) for k,v in main.make_autocomplete(c,line).items()]


#   def complete_cd_both(self,text,line,*args):
#     """
#       try
#        complete context sensitive,
#       if no mathches
#        complete context free
#     """
#     data = self.complete_cd(text,line)
#     if not data:
#       return self.complete_cd_tag_context_free(text)
#     return data



# #  def complete_cd(self,text,line):
# #    tags = self.cur_dir.join(' ')
# #    data = main.make_autocomplete(c,tags)
# #    if text && data:
# #      fuzzy_completed = main.fuzzy_autocomplete(word, data)
# #      if fuzzy_completed:
# #        return ["%s (%s)"%(i, data[i]) for i in fuzzy_completed]#

# #    return ["%s (%s)"%(v,k) for k,v in data.items()]



#   def do_bye(self,arg):
#     return True



# x = []
# class TestCmd(cmd.Cmd):
#   def do_hello(self,args):
#     print args

#   def complete_hello(self,text,line,*args):
#     print text
#     print line
#     return ['asd','bsd']

#   def do_bye(self,args):
#     return True

# TestCmd().cmdloop()
