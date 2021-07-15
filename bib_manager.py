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
import re
from datetime import datetime
from bib_table_of_contents import BibTableOfContents
from bib_reference import PublicationType, BibReference
from self_error import GeneralErrorMessage

AUTHOR_NAME = "SUN LU"

class BibManager:
    """
    Class BibManager defines a bib file management tool for LaTeX users.
    """
    def __init__(self):
        print("Welcome to BibManager.")
        self.path_bib = None
        self.obj_table_of_contents = BibTableOfContents()
        self.dict_refs = {}
    def set_path(self):
        """
        setpath sets the path to the bib file.
        """
        path_bib = input("Please enter the path to the bib file (e.g.: ./refs.bib): ")
        if os.path.isfile(path_bib):
            print("The path directs to an exsiting bib file...")
            if self.__ask_yes_no("Do you want to work on this bib file?"):
                print("The path has been confirmed. ")
                self.path_bib = path_bib
            else:
                print("Abort: the path is not saved.")
        else:
            print("There is no bib file found in the given path. " \
                  + "A new bib file is created. ")
            self.path_bib = path_bib
            with open(self.path_bib, 'w') as file_bib:
                file_bib.write('%% - Name of bib file: ' + self.path_bib.split('/')[-1])
    def read_bib(self):
        """
        readbib reads references items from self.path_bib, and store them in
        a 2D dictionary; if table of contents (metadata) exists, the table of
        contents is also read and stored in a 2D list.
        """
        print("Reading the bib file...")
        self.__read_table_of_contents_from_bib()
        self.__add_refs_from_bib()
    def show_table_of_contents(self):
        """
        show_talbe_of_contents shows the table of content in the console.
        """
        if self.obj_table_of_contents is None:
            print("There is no table of contents registered.")
        else:
            self.obj_table_of_contents.show_table_of_contents()
    def create_table_of_contents_from_console(self):
        """
        create_table_of_contents_from_console reads the table of contents 
        structure from the console and sets it as the new table of contents.
        """
        self.obj_talbe_of_contents = BibTableOfContents()
        print("Please key in the table of contents below. " + \
              "Use TAB(s) for sub sections. Enter a blank row to quit.")
        lst_console_inputs = []
        while True:
            try:
                str_console_input = input()
                if str_console_input == '':
                    break
            except EOFError:
                break
            lst_console_inputs.append(str_console_input)
        self.obj_table_of_contents.create_table_of_contents_from_console(
            lst_console_inputs)
        print("The following table of contents is created.")
        self.show_table_of_contents()
    def add_refs_from_console(self):
        """
        add_refs_from_console reads the reference information from the
        console and adds it to the reference dictionary.
        """
        print("Please key in the reference below. Register ONE reference only. " + \
              "Enter a blank row to quit.")
        lst_console_inputs = []
        while True:
            try:
                str_console_input = input()
                if str_console_input == '':
                    break
            except EOFError:
                break
            lst_console_inputs.append(str_console_input)
        lst_console_inputs = self.__chop_list(lst_console_inputs)
        self.__add_refs(lst_console_inputs)
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
                  The file will be over written.")
        if self.__ask_yes_no("Do you want to continue?"):
            print("Redirecting path to " + path_output_bib + "")
            self.path_bib = path_output_bib
            print("Updating bib file...")
            with open(self.path_bib, 'w') as file_bib:
                # time
                str_print = "%% - Latest updated time: " + \
                    datetime.now().strftime("%B %d, %Y %H:%M:%S")
                file_bib.write(str_print + "\n")
                print(str_print)
                # author
                str_print = "%% - Updated by: " + AUTHOR_NAME
                file_bib.write(str_print + "\n")
                print(str_print)
                # table of Contents
                if self.obj_table_of_contents is None:
                    str_print = "%% - Table of contents: None"
                    file_bib.write(str_print + "\n")
                    print(str_print)
                else:
                    str_list = "%% - Table of contents: "
                    file_bib.write(str_list + "\n")
                    print(str_list)
                    lst_print = self.obj_table_of_contents.return_table_of_contents()
                    for iter_item in lst_print:
                        str_list = "%% - > " + iter_item
                        file_bib.write(str_list + "\n")
                        print(str_list)
                    str_print = "%% - End of Table of Contents"
                    file_bib.write(str_print + "\n")
                    print(str_print)
            # references
        else:
            print("Abort: The bib file is not updated.")
    def __read_table_of_contents_from_bib(self):
        pass
    def __add_refs_from_bib(self):
        with open(self.path_bib, 'r') as file_bib:
            lst_file_inputs = file_bib.readlines()
            lst_file_inputs = [str_fileinput.strip() 
                               for str_fileinput in lst_file_inputs]
        self.__add_refs(lst_file_inputs)
    def __add_refs(self, lst_text):
        for iter_item in lst_text:
            if len(iter_item) > 0:
                # type and id
                lst_keyinfo = re.findall('@.*{', iter_item)
                if len(lst_keyinfo) > 0:
                    obj_reference = BibReference()
                    obj_reference.str_type = lst_keyinfo[0][1:-1].lower()
                    if obj_reference.str_type == 'book':
                        obj_reference.enum_type = PublicationType(1)
                    elif obj_reference.str_type == 'article':
                        obj_reference.enum_type = PublicationType(2)
                    elif obj_reference.str_type == 'inproceedings':
                        obj_reference.enum_type = PublicationType(3)
                    elif obj_reference.str_type == 'online':
                        obj_reference.enum_type = PublicationType(4)
                    else:
                        obj_reference.enum_type = PublicationType(5)
                lst_keyinfo = re.findall('@.*{.*,', iter_item)
                if len(lst_keyinfo) > 0:
                    lst_keyinfo = re.findall('{.*,', lst_keyinfo[0])
                    obj_reference.str_id = lst_keyinfo[0][1:-1]
                # title
                lst_keyinfo = re.findall('title ?= ?{.*}', iter_item)
                if len(lst_keyinfo) > 0:
                    lst_keyinfo = re.findall('{.*}', lst_keyinfo[0])
                    obj_reference.str_title = lst_keyinfo[0][1:-1]
                # author
                lst_keyinfo = re.findall('author ?= ?{.*}', iter_item)
                if len(lst_keyinfo) > 0:
                    lst_keyinfo = re.findall('{.*}', lst_keyinfo[0])
                    obj_reference.str_author = lst_keyinfo[0][1:-1]
                # journal
                lst_keyinfo = re.findall('journal ?= ?{.*}', iter_item)
                if len(lst_keyinfo) > 0:
                    lst_keyinfo = re.findall('{.*}', lst_keyinfo[0])
                    obj_reference.str_journal = lst_keyinfo[0][1:-1]
                # volume
                lst_keyinfo = re.findall('volume ?= ?{.*}', iter_item)
                if len(lst_keyinfo) > 0:
                    lst_keyinfo = re.findall('{.*}', lst_keyinfo[0])
                    obj_reference.str_volume = lst_keyinfo[0][1:-1]
                # number
                lst_keyinfo = re.findall('number ?= ?{.*}', iter_item)
                if len(lst_keyinfo) > 0:
                    lst_keyinfo = re.findall('{.*}', lst_keyinfo[0])
                    obj_reference.str_number = lst_keyinfo[0][1:-1]
                # pages
                lst_keyinfo = re.findall('pages ?= ?{.*}', iter_item)
                if len(lst_keyinfo) > 0:
                    lst_keyinfo = re.findall('{.*}', lst_keyinfo[0])
                    obj_reference.str_pages = lst_keyinfo[0][1:-1]
                # year
                lst_keyinfo = re.findall('year ?= ?{.*}', iter_item)
                if len(lst_keyinfo) > 0:
                    lst_keyinfo = re.findall('{.*}', lst_keyinfo[0])
                    obj_reference.str_year = lst_keyinfo[0][1:-1]
                # publisher
                lst_keyinfo = re.findall('publisher ?= ?{.*}', iter_item)
                if len(lst_keyinfo) > 0:
                    lst_keyinfo = re.findall('{.*}', lst_keyinfo[0])
                    obj_reference.str_publisher = lst_keyinfo[0][1:-1]
                # end of reference / hex_catid
                if iter_item[0] == '}':
                    lst_keyinfo = re.findall('% catid = \d{8}', iter_item)
                    if len(lst_keyinfo) > 0:
                        lst_keyinfo = re.findall('\d{8}', lst_keyinfo[0])
                        obj_reference.hex_catid = int(lst_keyinfo[0])
                    self.dict_refs[obj_reference.str_id] = obj_reference
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
    @staticmethod
    def __chop_list(lst_input):
        lst_output = []
        for iter_item in lst_input:
            lst_chopped = iter_item.split('\n')
            lst_output = lst_output + lst_chopped
        return lst_output
