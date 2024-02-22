# -*- coding: utf-8 -*-
"""
Class BibManager defines a bib file managing tool for LaTeX users. Class BibManager
can create/open a bib file, and do the followings:
- read existing references and table of contents (if exists; stored as
metadata) in the bib file;
- create table of contents;
- show table of contents;
- add a new reference;
- search/edit/remove an existing reference;
- categorize reference;
- sort references;
- global search and replace, e.g. "GUI" to "{GUI}" in title, "System" to "Syst." in journal;
- (optional) statistics analysis, such as distribution by year
- (optional) graphical user interface
- (optional) synchronize with Google Scholar;
- generate/update the bib file.
"""

import os
import re
from datetime import datetime
from bib_table_of_contents import BibTableOfContents
from bib_reference import PublicationType, BibReference

AUTHOR_NAME = "SUN LU"


class BibManager:
    """
    Class BibManager defines a bib file management tool for LaTeX users.
    """

    def __init__(self):
        self.path_bib = None
        self.obj_tocs = BibTableOfContents()
        self.obj_tocs.create_tocs_from_multidimensional_list(
            ['Default Section'])
        self.dict_refs = {}
        self.dict_refs_categorized = {}

    def set_path(self, path_bib):
        """
        set_path sets the path to the bib file.
        """
        if os.path.isfile(path_bib):
            pass
        else:
            with open(self.path_bib, 'w') as file_bib:
                file_bib.write("%% - Name of bib file: " +
                               self.path_bib.split('/')[-1] + "\n")
        self.path_bib = path_bib
        print("The path to the bib file has been confirmed.")

    def set_path_from_console(self):
        """
        set_path_from_console sets the path to the bib file from console.
        """
        print("Current working directory is: " + os.getcwd())
        path_bib = input(
            "Please enter the path to the bib file (e.g.: ./refs.bib):\n")
        if os.path.isfile(path_bib):
            print("The path directs to an existing bib file. ", end="")
            print("There is a chance that the file be overwritten later.")
            if self.__ask_yes_no("Do you want to continue with the path?"):
                self.path_bib = path_bib
                print("The path to the bib file has been confirmed.")
            else:
                print("Abort. The path to the bib file is canceled.")
        else:
            self.path_bib = path_bib
            print("The path to the bib file has been confirmed.\
                  A new bib file will be created at " + self.path_bib)
            with open(self.path_bib, 'w') as file_bib:
                file_bib.write("%% - Name of bib file: " +
                               self.path_bib.split('/')[-1] + "\n")
            print("A new bib file has been created at " + self.path_bib)

    def read_bib(self):
        """
        readbib reads references items from self.path_bib, and store them in
        a 2D dictionary; if table of contents (metadata) exists, the table of
        contents is also read and stored in a 2D list.
        """
        print("Reading the bib file at " + self.path_bib)
        print("Reading table of contents from the bib file...")
        self.__read_tocs_from_bib()
        print("Adding references from the bib file...")
        self.__add_refs_from_bib()
        print("A total of " + str(len(self.dict_refs)) +
              " publication(s) have been registered.")
        print("Reading completed.")

    def display_tocs(self):
        """
        display_tocs shows the table of content in the console.
        """
        self.obj_tocs.display_tocs()

    def update_tocs_from_console(self):
        """
        update_tocs_from_console reads the table of contents structure from the
        console and sets it as the new table of contents.
        """
        print("Please key in the table of contents below. ", end="")
        print("Use four (4) spaces for sub sections of each layer. Enter a blank row to quit and save the editing.")
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
        self.__update_tocs(lst_console_inputs)
        print("The following table of contents has been created.")
        self.display_tocs()

    def add_refs_from_console(self):
        """
        add_refs_from_console reads the reference information from the
        console and adds it to the reference dictionary.
        """
        print("Please key in the reference(s) below. ", end="")
        print("Enter a blank row to quit.")
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

    def update_catid(self, strlst_id: str):
        """
        update_catid updates the catid for one or multiple references, depending
        on whether str_id or lst_id is used as input.
        """
        if isinstance(strlst_id, str):
            if strlst_id == 'uncategorized':
                self.update_dict_refs_categorized()
                lst_id = list(self.dict_refs_categorized[-1].keys())
                for iter_item in lst_id:
                    if not self.__update_catid(iter_item):
                        break
            else:
                self.__update_catid(strlst_id)
        elif isinstance(strlst_id, list):
            for iter_item in lst_id:
                _ = self.__update_catid(iter_item)
        else:
            print('It is not clear which reference catid shall be updated.')

    def update_dict_refs_categorized(self):
        """
        update_dict_refs_categorized updates self.dict_refs_categorized using
        the table of contents and the registered refs catid
        The keys of self.dict_refs_categorized are the leafs of the table of
        contents. Uncategorized/Wrongly categorized refs are put into separate
        categories.
        """
        self.dict_refs_categorized = {}
        lst_tocs_all_keys = self.obj_tocs.return_tocs_all_keys()
        lst_tocs_leaf_keys = self.obj_tocs.return_tocs_leaf_keys()
        self.dict_refs_categorized[-1] = {}  # Refs uncategorized
        self.dict_refs_categorized[-2] = {}  # Refs with unrecognized catid
        self.dict_refs_categorized[-3] = {}  # Refs categorized not under leaf
        if lst_tocs_leaf_keys is not None:
            for iter_item in lst_tocs_all_keys:
                self.dict_refs_categorized[iter_item] = {}
            for iter_key, iter_value in self.dict_refs.items():
                if iter_value.hex_catid is None:
                    self.dict_refs_categorized[-1][iter_key] = iter_value
                elif iter_value.hex_catid not in lst_tocs_all_keys:
                    self.dict_refs_categorized[-2][iter_key] = iter_value
                elif iter_value.hex_catid not in lst_tocs_leaf_keys:
                    self.dict_refs_categorized[-3][iter_key] = iter_value
                else:
                    self.dict_refs_categorized[iter_value.hex_catid][iter_key] = iter_value
        else:
            print("Table of contents needs to be defined before categorization.")

    def update_bib(self, path_output_bib='default', str_author_name=AUTHOR_NAME):
        """
        update_bib updates the bib file, including:
        - print the path to the updated bib file (by default the same path as
        self.path_bib, unless otherwise specified);
        - generate time author name stamps in the bib file;
        - print table of content in the bib file;
        - (optional, by default) sort the references;
        - print references in the bib file.
        """
        self.update_dict_refs_categorized()
        if path_output_bib == 'default':
            path_output_bib = self.path_bib
        print("The updated bib file will be stored at " + path_output_bib)
        if os.path.isfile(path_output_bib):
            print(
                "Warning: This path points to an existing file. The file will be over written.")
        if self.__ask_yes_no("Do you want to continue with the path?"):
            self.path_bib = path_output_bib
            print("Updating bib file...")
            with open(self.path_bib, 'w') as file_bib:
                # name
                file_bib.write("%% - Name of bib file: " +
                               self.path_bib.split('/')[-1] + "\n")
                # time
                str_print = "%% - Latest updated time: " + \
                    datetime.now().strftime("%B %d, %Y %H:%M:%S")
                file_bib.write(str_print + "\n")
                print(str_print)
                # author
                str_print = "%% - Updated by: " + str_author_name
                file_bib.write(str_print + "\n")
                print(str_print)
                # table of Contents
                if self.obj_tocs is None:
                    str_print = "%% - Table of Contents: None"
                    file_bib.write(str_print + "\n")
                else:
                    str_list = "%% - Table of Contents"
                    file_bib.write(str_list + "\n")
                    lst_print = self.obj_tocs.return_tocs_printout()
                    for iter_item in lst_print:
                        str_list = "%% - > " + iter_item
                        file_bib.write(str_list + "\n")
                    str_print = "%% - End of Table of Contents"
                    file_bib.write(str_print + "\n")
                    file_bib.write("\n")
                # references
                lst_tocs_print = list(self.dict_refs_categorized.keys())
                lst_tocs_print.sort()
                for iter_item in lst_tocs_print:
                    if iter_item > 0:
                        file_bib.write("\n")
                        file_bib.write("%% - " + hex(iter_item) + " " +
                                       self.obj_tocs.dict_tocs[iter_item] + "\n")
                        lst_tocs_sublayer_print = list(
                            self.dict_refs_categorized[iter_item])
                        lst_tocs_sublayer_print.sort()
                        for iter_item_sublayer in lst_tocs_sublayer_print:
                            lst_print = self.dict_refs_categorized[iter_item][iter_item_sublayer].return_refs_printout(
                            )
                            file_bib.write("\n")
                            for str_print in lst_print:
                                file_bib.write(str_print + "\n")
                file_bib.write("\n")
                file_bib.write("%% - " + "Uncategorized references" + "\n")
                lst_tocs_sublayer_print = list(self.dict_refs_categorized[-1])
                lst_tocs_sublayer_print.sort()
                for iter_item_sublayer in lst_tocs_sublayer_print:
                    lst_print = self.dict_refs_categorized[-1][iter_item_sublayer].return_refs_printout(
                    )
                    file_bib.write("\n")
                    for str_print in lst_print:
                        file_bib.write(str_print + "\n")
                file_bib.write("\n")
                file_bib.write(
                    "%% - " + "References categorized not under leaf" + "\n")
                lst_tocs_sublayer_print = list(self.dict_refs_categorized[-3])
                lst_tocs_sublayer_print.sort()
                for iter_item_sublayer in lst_tocs_sublayer_print:
                    lst_print = self.dict_refs_categorized[-3][iter_item_sublayer].return_refs_printout(
                    )
                    file_bib.write("\n")
                    for str_print in lst_print:
                        file_bib.write(str_print + "\n")
                file_bib.write("\n")
                file_bib.write("%% - " + "Unrecoganized catid" + "\n")
                lst_tocs_sublayer_print = list(self.dict_refs_categorized[-2])
                lst_tocs_sublayer_print.sort()
                for iter_item_sublayer in lst_tocs_sublayer_print:
                    lst_print = self.dict_refs_categorized[-2][iter_item_sublayer].return_refs_printout(
                    )
                    file_bib.write("\n")
                    for str_print in lst_print:
                        file_bib.write(str_print + "\n")
        else:
            print("Abort. The bib file is not updated.")

    def __read_tocs_from_bib(self):
        with open(self.path_bib, 'r') as file_bib:
            lst_file_inputs = file_bib.readlines()
            lst_file_inputs = [str_fileinput.strip()
                               for str_fileinput in lst_file_inputs]
        flag_detect_tocs = False
        lst_text = []
        for iter_item in lst_file_inputs:
            if iter_item == "%% - Table of Contents":
                flag_detect_tocs = True
                continue
            if iter_item == "%% - End of Table of Contents":
                break
            if flag_detect_tocs:
                lst_text.append(iter_item[7:])
        if flag_detect_tocs:
            self.__update_tocs(lst_text)
            print("The following table of contents has been created.")
            self.display_tocs()
        else:
            print("Table of contents is not detected from the bib file.", end="")
            print("A default table of contents has been created.")
            self.obj_tocs = BibTableOfContents()
            self.obj_tocs.create_tocs_from_multidimensional_list(
                ['Default Section'])
            self.display_tocs()

    def __add_refs_from_bib(self):
        with open(self.path_bib, 'r') as file_bib:
            lst_file_inputs = file_bib.readlines()
            lst_file_inputs = [str_fileinput.strip()
                               for str_fileinput in lst_file_inputs]
        self.__add_refs(lst_file_inputs)

    def __update_catid(self, str_id):
        if str_id in self.dict_refs:
            str_catid = input(
                "Please key in the catid for reference " + str_id + ": 0x")
            try:
                self.dict_refs[str_id].hex_catid = int(str_catid, 16)
                return True
            except:
                return False
        print("Reference " + str_id + " cannot be found.")
        return False

    def __update_tocs(self, lst_text):
        self.obj_tocs = BibTableOfContents()
        self.obj_tocs.create_tocs_from_space_list(lst_text)

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
                    lst_keyinfo = re.findall(r'% catid = 0x\d{8}', iter_item)
                    if len(lst_keyinfo) > 0:
                        lst_keyinfo = re.findall(r'0x\d{8}', lst_keyinfo[0])
                        obj_reference.hex_catid = int(lst_keyinfo[0], 0)
                    self.dict_refs[obj_reference.str_id] = obj_reference

    @staticmethod
    def __ask_yes_no(str_message):
        while True:
            str_input = input(str_message + " (YES/NO): ")
            if str_input.upper() == 'YES':
                return True
            elif str_input.upper() == 'NO':
                return False
            else:
                print("Please reply with either YES or NO.")

    @staticmethod
    def __chop_list(lst_input):
        lst_output = []
        for iter_item in lst_input:
            lst_chopped = iter_item.split('\n')
            lst_output = lst_output + lst_chopped
        return lst_output
