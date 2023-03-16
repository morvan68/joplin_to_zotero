#@+leo-ver=5-thin
#@+node:martin.20210515201503.2: * @file ./j_to_z.py
#@@language python
#@@tabwidth -4

#@+others
#@+node:martin.20210605192255.2: ** imports
import os
import sys
import argparse
import pprint      

from functools import reduce

from pyzotero import zotero

#@+node:martin.20230313204450.1: ** utilities
def get_all_keys(d):
    """
    https://stackoverflow.com/questions/43752962/how-to-iterate-through-a-nested-dict
    """
    for key, value in d.items():
        yield key
        if isinstance(value, dict):
            yield from get_all_keys(value)


def print_dict(v, prefix=''):
    """
    https://stackoverflow.com/questions/10756427/loop-through-all-nested-dictionary-values
    keeps track of paths, ideal!
    """
    if isinstance(v, dict):
        for k, v2 in v.items():
            p2 = "{}/{}".format(prefix, k)
            yield from print_dict(v2, p2)
    else:
        yield prefix#, repr(v)))


def myprint(d):
    """
    https://stackoverflow.com/questions/10756427/loop-through-all-nested-dictionary-values
    """
    for k, v in d.items():
        if isinstance(v, dict):
            print( k)
            myprint(v)
        else:
            print("{0} : {1}".format(k, v))


def myprint_i(d):
    """
    https://stackoverflow.com/questions/10756427/loop-through-all-nested-dictionary-values
    iterative version
    python 2 only. cant pop a dict key in py3
    """
    stack = d.items()
    while stack:
        k, v = stack.pop()
        if isinstance(v, dict):
            stack.extend(v.iteritems())
        else:
            print("%s: %s" % (k, v))
#@+node:martin.20211211160450.1: ** mdtree_to_dict
def mdtree_to_dict (rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    #https://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
    dir_dict = {}
    dir_dict['basedir'] = rootdir
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

#    print_dict( mydict)
    
    #pprint.pprint( mydict)
        
#    for i in mydict:
#        print( mydict[i])
    return
#@+node:martin.20210605192255.3: ** dict_to_z
def dict_to_z( sdict, api_key, library_id):
    """
    write dict of notes to zotero collection
    currently does not support tags
    CAUTION - for pattern matching, assumes collection names are unique, even in subcollections!
    """
    if sdict == {} or sdict == None:
        print( 'empty call')
        exit()
    rootdir = sdict.pop('basedir')
    rootdir =  rootdir.split( os.sep)[:-1]
    rootdir = '/'.join( rootdir)
    print('root, ', rootdir)
    library_type = 'group'
    zot = zotero.Zotero(library_id, library_type, api_key)
    #check for valid item types
#    items = zot.item_types( )
#    print( ['{}\n\n'.format( items[a] ) for a in items] )
    
    # lets get some example items to get a feel for the format
#    things = zot.top( limit = 4)
#    for i in things:
#        print( i )
#    exit()
    
    rootitems = zot.collections()
    lut = {} #simple look up table for keys->collection names
    for a in rootitems:
        print( a['data']['key'], a['data']['name'], a['data']['parentCollection'])
        lut[ a['data']['name'] ] = a['data']['key']
    print('lut created')
    
    for item in print_dict( sdict):
        print( 'loading, ', item)
        if item.endswith('.md'):
            title = item[1:-3].split( os.sep)[-1]
            print('title, ', title)
            fname = os.path.join( rootdir, item.lstrip('/') )
            print('fn, ', fname)
            destdir = fname.split( os.sep)[-2]
            print( 'dest, ', destdir)           
            with open( fname, 'rt') as fp:
                content = fp.readlines()
            print('loaded, ', item)
#            print('contents, ', content)
            i = zot.item_template('note')
            i['note'] = '</p>\n<p>'.join( content) #put breaks in md string
            i['note'] ='<p>' + i['note'] + '</p>'           
            # use lut to set collection
            coll = lut[ destdir]
            i['collections'].append( coll) 
            #checking
            print( 'zot item, ', i)
            zot.check_items( [i] ) #given list of 1 item, raises error if wrong
            if api_key != 'dummy': 
                print( 'creating, ', title)
                result = zot.create_items( [i] ) #send a list of 1 dict
                if result == []:
                    print('failed, ', title)
                else:
                    print( 'created')
            else:
                print( 'fake creating, ', title)
#            exit() #just do one
        else:
            pass
    return
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
    parser = argparse.ArgumentParser(
                    prog='files to zotero',
                    description='What the program does')
    
    parser.add_argument('sourcedir')
    parser.add_argument('-id', '--library_id')
    parser.add_argument('-api', '--api_key', default = 'dummy')
    parser.add_argument('-js', '--JSON', default=False)

    args = parser.parse_args()
    sourcedir = args.sourcedir
    library_id = args.library_id
    api_key = args.api_key
    if args.JSON:
        md_dict = j_to_z_json( sourcedir, api_key)
    else:
        print('making dict')
        md_dict = mdtree_to_dict( sourcedir)
        print('to z')
        dict_to_z( md_dict, api_key, library_id)
        print('done')
#@-others
#@-leo
