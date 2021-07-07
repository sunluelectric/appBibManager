# -*- coding: utf-8 -*-
"""
Class BibManager defines a bib file managing tool for LaTeX users. 
Class BibManager can create/open a bib file, and do the followings:
- read existing references and table of contents (if exists; stored as
metadata) in the bib file;
- create/show tree-structure table of contents;
- insert a new reference into the bib file;
- search/edit/remove an existing reference;
- sort references;
- global replace, e.g. "GUI" to "{GUI}" in title, "System" to "Syst." in journal;
- (optional) syncronize with Google Scholar;
- generate/update the bib file.
@author: github.com/sunluelectric
"""

import os
from bib_table_of_contents import BibTableOfContents

class BibManager:
    """
    Class BibManager defines a bib file management tool for LaTeX users.
    """
    def __init__(self):
        print("Welcome to BibManager.\n")
        print("Initializing...\n")
        self.path_bib = None
        self.obj_table_of_contents = None
        self.dict_refs = None
    def set_path(self):
        """
        setpath sets the path to the bib file.
        """
        path_bib = input("Please enter the path to the bib file (e.g.: ./refs.bib): ")
        if os.path.isfile(path_bib):
            print("The path directs to an exsiting bib file...\n")
            if self.__ask_yes_no("Do you want to work on this bib file?"):
                print("The path has been confirmed. \n")
                self.path_bib = path_bib
                return 0
            else:
                print("The path has been aborted.")
                return 1
        else:
            print("There is no bib file found in the given path. " \
                  + "A new bib file is created. \n")
            self.path_bib = path_bib
            file_bib = open(self.path_bib, 'w')
            file_bib.write('%% ' + self.path_bib.split('/')[-1] + ' %%' + '\n')
            file_bib.close()
            return 0
    def read_bib(self):
        """
        readbib reads references items from self.path_bib, and store them in
        a 2D dictionary; if table of contents (metadata) exists, the table of
        contents is also read and stored in a 2D list.
        """
        print("Reading the bib file...")
        # self.obj_table_of_contents = ?
        # self.lst_refs = ?
        pass
    
    def edit_table_of_contents(self):
        """
        edit_table_of_contents creates or edits the table of contents of the
        bib file.
        """
        if self.obj_table_of_contents is None:
            print("There is no table of contents registered. " + \
                  "Please input the designed table of content below.\n")
            self.set_table_of_contents()
        else:
            print("Existing table of contents is shown below.\n")
            self.show_table_of_contents()
            if self.__ask_yes_no("Do you want to edit the table of contents?"):
                print("Please input the designed table of content below.\n")
                self.set_table_of_contents()
            else:
                print("The table of contents remains unchanged.\n")
    def show_table_of_contents(self):
        """
        show_talbe_of_contents shows the table of content in the console.
        """
        if self.obj_table_of_contents is None:
            print("There is table of contents registered.\n")
        else:
            self.obj_table_of_contents.show_table_of_contents()
    def set_table_of_contents(self):
        """
        set_table_of_content reads the table of contents structure from the 
        console and set it as the new table of contents.
        """
        self.obj_talbe_of_contents = BibTableOfContents()
        lst_table_of_contents_concatenated = self.__input_concatenated_list()
        self.obj_talbe_of_contents.create_table_of_contents(
            lst_table_of_contents_concatenated)
        pass
    
    
    def __ask_yes_no(str_message):
        str_input = input(str_message + " (YES/NO): ")
        while True:
            if str_input.upper() == 'YES':
                return True
            elif str_input.upper() == 'NO':
                return False
            else:
                str_input = input("Please reply with YES or NO: ")
    def __input_concatenated_list():
        lst_concatenated = []
        return lst_concatenated
