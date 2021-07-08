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
from datetime import datetime
from bib_table_of_contents import BibTableOfContents

AUTHOR_NAME = "SUN LU"

class BibManager:
    """
    Class BibManager defines a bib file management tool for LaTeX users.
    """
    def __init__(self):
        print("Welcome to BibManager.\n")
        print("Initializing...\n")
        self.path_bib = None
        self.obj_table_of_contents = BibTableOfContents()
        # self.dict_refs = None
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
                print("Abort: the path is not saved.")
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
    def show_table_of_contents(self):
        """
        show_talbe_of_contents shows the table of content in the console.
        """
        if self.obj_table_of_contents is None:
            print("There is no table of contents registered.\n")
        else:
            self.obj_table_of_contents.show_table_of_contents()
    def set_table_of_contents(self):
        """
        set_table_of_content reads the table of contents structure from the 
        console and set it as the new table of contents.
        """
        self.obj_talbe_of_contents = BibTableOfContents()
        self.obj_table_of_contents.create_table_of_contents_from_console()
        print("The following table of contents is created.\n")
        self.show_table_of_contents()
    def update_bib(self, path_output_bib = 'default', str_author_name = AUTHOR_NAME):
        """
        update_bib updates the bib file, including:
        - print the path to the updated bib file (by default the same path as
        self.path_bib, unless otherwise specified);
        - generate time author name stamps in the bib file;
        - print table of content in the bib file;
        - (optional, by default) sort the references;
        - print references in the bib file.
        """
        if path_output_bib == 'default':
            path_output_bib = self.path_bib
        print("The updated bib file will be stored at " + path_output_bib)
        if os.path.isfile(path_output_bib):
            print("Warning: This path points to an existing file. \
                  The file will be over written.\n")
        if self.__ask_yes_no("Do you want to continue?"):
            print("Redirecting path to " + path_output_bib + "\n")
            self.path_bib = path_output_bib
            print("Updating bib file...\n")
            file_bib = open(self.path_bib, 'w')
            # time
            str_print = "%% - Latest Updated Time: " + \
                datetime.now().strftime("%B %d, %Y %H:%M:%S") + "\n"
            file_bib.write(str_print)
            print(str_print)
            # author
            str_print = "%% - Updated by: " + AUTHOR_NAME + "\n"
            file_bib.write(str_print)
            print(str_print)
            # table of Contents
            if self.obj_table_of_contents is None:
                str_print = "%% - Table of Contents: None \n"
                file_bib.write(str_print)
                print(str_print)
            else:
                str_list = "%% - Table of Contents\n"
                file_bib.write(str_list)
                print(str_list)
                lst_print = self.obj_table_of_contents.return_table_of_contents()
                for iter_item in lst_print:
                    str_list = "%% - > " + iter_item
                    file_bib.write(str_list)
                    print(str_list)
                str_print = "%% - End of Table of Contents\n"
                file_bib.write(str_print)
                print(str_print)
            # references
            file_bib.close()
        else:
            print("Abort: The bib file is not updated.\n")
    @staticmethod
    def __ask_yes_no(str_message):
        str_input = input(str_message + " (YES/NO): ")
        while True:
            if str_input.upper() == 'YES':
                return True
            elif str_input.upper() == 'NO':
                return False
            else:
                str_input = input("Please reply with either YES or NO: ")
