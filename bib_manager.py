# -*- coding: utf-8 -*-
"""
Class BibManager defines a bib file management tool for LaTeX users. 
Class BibManager can create/open a bib file, and do the followings:
- read existing references and table of contents (if exists; stored as
metadata) in the bib file;
- create/show tree-structure table of contents;
- insert a new reference into the bib file;
- search/edit/remove an existing reference;
- sort references;
- global replace, e.g. "GUI" to "{GUI}" in title, "System" to "Syst." in journal;
- (optional) syncronize with google scholar;
- generate/update the bib file.
@author: sunlu.electric@gmail.com
"""

import os

class BibManager:
    """
    Class BibManager defines a bib file management tool for LaTeX users.
    """
    def __init__(self):
        print("Welcome to BibManager.\n")
        print("Initializing...\n")
        self.path_bib = None
        self.lst_table_of_contents = None
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
        # self.lst_table_of_contents = ?
        # self.lst_refs = ?
        pass
    
    def edit_table_of_contents(self):
        """
        edit_table_of_contents creates or edits the table of contents of the
        bib file.
        """
        if self.lst_table_of_contents is None:
            print("No table of contents has been defined. " + \
                  "Please input the designed table of content below.\n")
            # self.lst_talbe_of_content = ?
        else:
            print("Existing table of contents is displayed as below.\n")
            self.show_table_of_contents()
            if self.__ask_yes_no("Do you want to edit the table of contents?"):
                print("Please input the designed table of content below.\n")
                # self.lst_talbe_of_content = ?
            else:
                print("The table of contents remains unchanged.\n")
    def show_table_of_contents(self):
        """
        show_talbe_of_contents shows the table of content in the console.
        """
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
    def __inputmultipleline():
        lst_input = []
