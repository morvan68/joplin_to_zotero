# joplin_to_zotero
small utility to move notes from joplin to a collection within zotero
(or more generally create a collection within zotero based on a folder structure with text/md files)

md version
----------
in joplin, run 
    joplin export all as md
This builds a folder tree with your exported joplin notes as md files within substructures

Then the main script j_to_z.py will walk this folder tree and create same structure within zotero
note that tags are not transferred when using md version

json version
------------
in joplin run 
    TBD joplin export 
this creates a flat folder with json files with all the tags/parent structure embedded.
import not yet implemented, but will support tags

