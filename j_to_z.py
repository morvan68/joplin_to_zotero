#@+leo-ver=5-thin
#@+node:martin.20210515201503.2: * @file ./j_to_z.py
#@@language python
#@@tabwidth -4

#@+others
#@+node:martin.20210605192255.2: ** Declarations (j_to_z.py)
import os
import sys

from pyzotero import zotero

#@+node:martin.20210605192255.3: ** j_to_z (j_to_z.py)
def mdtree_to_z( sdir , api_key):
    """
    md option (it looses any tags)
    before running:
    
    joplin export all as md
    
    """
    # load text items from sdir to import them
    #this needs to be walk, to build a dict/subdict tree structure
    loaded_dict = {}
    
    loaded_dict = dir_to_dict( sdir)    

    print( loaded_dict)

    library_id = ''
    library_type = ''
    zot = zotero.Zotero(library_id, library_type, api_key)

    items = zot.top(limit=5)
    # we've retrieved the latest five top-level items in our library
    # we can print each item's item type and ID
    if items == [] or items == None:
        print( 'something failed')
        exit()
    for item in items:
        print('Item: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))
    
      
    
    exit()
        
        #recurs the dict, sending item to zotero
        #or can we do the whole dict in one go??
        
        #zot.create_items( loaded_items[, parentid, last_modified])
            #create a thing, need to poll parent to get parent_id

"""
            items (list) – one or more dicts containing item data
            parentid (str) – A Parent item ID. This will cause the item(s) to become the child items of the given parent ID
            last_modified (str/int) – If not None will set the value of the If-Unmodified-Since-Version header.
"""

#@+node:martin.20211211160450.1: ** dir_to_dict
def dir_to_dict (rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    #https://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
    dir_dict = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        
        subdir = dict.fromkeys(files)
        
        parent = reduce( dict.get, folders[:-1], dir_dict)

        parent[ folders[-1]] = subdir
    
    return dir_dict

"""    
        for ii in filenames:
#           read each md, save as standalonenote using api
            if  ii.endswith('.md'):
                with open( os.path.join( dirpath, ii), 'rt') as fp:
                    xx = fp.readlines()
                    print( ii, '\n------\n', xx)
                    loaded_dict[dirpath][ii[:-4]] = xx
    #not lets print what we've got to check
"""


#@+node:martin.20210605234949.1: ** j_to_z_json
def j_to_z_json( sdir, api_key):
    ...
    """
    tag supporting option
    #jopline export as json
    
    reald local folder
                read jsons
                build data structure in memory as json/dicts
                connect to api
                write all the tags to collection
                write subcollectiosn, itesms, tags
    """

#@+node:martin.20210605192456.1: ** main
if __name__ == '__main__':
    sourcedir = sys.argv[1]
    api_key = sys.argv[2]
    mdtree_to_z( sourcedir, api_key)

    
#@-others
#@-leo
