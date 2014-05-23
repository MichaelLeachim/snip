#Vars from this file will be available on all other files 
import os 
HOME_DIR                 = '/home/mik/test/'
DEFAULT_EDITOR           = 'vim'
DEFAULT_FOLDER_NAME      = ".snip"
NODES_FOLDER             = "nodes"
PROGRAM_FOLDER           = "/home/mik/test/.snip/"
TAG_SPLITTER             = ' '
FROM_DISK_PARSE_PATTERN  = """
    ~::::
      (?P<rowid>ID-[0-9]+\s)?
      (?P<tags>.*?)
    ::::~
    (?P<node>.*?)
    ==========
"""
TO_DISK_FLUSH_PATTERN   = """
~::::ID-{rowid} {tags}::::~
{node}
==========
"""





