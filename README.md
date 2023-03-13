# joplin_to_zotero
Small utility to create a collection within online zotero based on
a local folder structure+text files, or a flat JSON folder.

This can be used to to move notes from joplin to a collection within zotero,
by using joplin to export its data as a md or JSON, then using this script
to import into zotero.

requirements:
python3
pyzotero
you need an online zotero desitnation, and api_key, and need to know colelctio type
and destination sub-collection

## md version
in joplin, run 
    joplin export all as md
This builds a folder tree with your exported joplin notes as md files within substructures

Then the main script j_to_z.py will walk this folder tree and create same structure within zotero.

Note that tags are not transferred when using md version

python3 j_to_z.py /path/to/base_folder API_KEY

## json version
in joplin run 
    TBD joplin export

this creates a flat folder with json files with all the tags/parent structure embedded.
j_to_z will then support tag import into zotero.

not yet implemented...

python3 j_to_z.py /path/to/base_folder API_KEY JSON

