#@+leo-ver=5-thin
#@+node:martin.20210515201503.2: * @file ./j_to_z.py
#@@language python
#@@tabwidth -4

#@+others
#@+node:martin.20210605192255.2: ** Declarations (j_to_z.py)
import os
import sys

from functools import reduce

from pyzotero import zotero

#@+node:martin.20211211160450.1: ** mdtree_to_dict
def mdtree_to_dict (rootdir):
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
    
    ###
    test_print( dir_dict)
    ###
    
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


#@+node:martin.20230313081000.1: ** test_print
def test_print( mydict):
    """used in testing to check the dict is correctly constructed based
    on the importing"""

    import pprint      
    pprint.pprint( mydict)
        
#    for i in mydict:
#        print( mydict[i])
#@+node:martin.20210605192255.3: ** dict_to_z
def dict_to_z( sdict , api_key):
    """
    write dict to zotero collection
    currently does not support tags
    """
    library_id = ''
    library_type = ''
    zot = zotero.Zotero(library_id, library_type, api_key)


    if items == [] or items == None:
        print( 'something failed')
        exit()
    for item in items:
        print('Item: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))
        
        if item.endswith('.md'):
            #its a file
            #load the file
            title = item[:-3]
        else:
            #its a sub dict
            ...
            
            #zot.create_items( loaded_items[, parentid, last_modified])
            #create a thing, need to poll parent to get parent_id

"""
    items (list) – one or more dicts containing item data
    parentid (str) – A Parent item ID. This will cause the item(s) to become the child items of the given parent ID
    last_modified (str/int) – If not None will set the value of the If-Unmodified-Since-Version header.

    items = zot.top(limit=5)
    # we've retrieved the latest five top-level items in our library
    # we can print each item's item type and ID

"""

#@+node:martin.20210605234949.1: ** j_to_z_json
def j_to_z_json( sdir, api_key):
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
    if len(sys.argv) > 2:
        api_key = sys.argv[2]
    else:
        api_key = 'dummy'
    if len(sys.argv) > 3 and sys.argv[3] == 'JSON':
        md_dict = j_to_z_json( sourcedir, api_key)
    else:
        md_dict = mdtree_to_dict( sourcedir)
        #dict_to_z( md_dict, api_key)
#@-others
#@-leo
