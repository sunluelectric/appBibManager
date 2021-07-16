# -*- coding: utf-8 -*-
"""
Class BibTableOfContents is a dataclass used to record the metadata for
table of contents information used in class BibManager.
@author: github.com/sunluelectric
"""

from dataclasses import dataclass
from self_error import GeneralErrorMessage

@dataclass
class BibTableOfContents:
    """
    Class BibTableOfContents is a dataclass used to record the metadata for
    table of contents information used in class BibManager.
    """
    hex_current_layer_index : int
    int_current_layer_pointer : int
    dict_tocs : dict
    def __init__(self):
        self.hex_current_layer_index = 0x00000000
        self.int_current_layer_pointer = 0
        self.dict_tocs = {}
    def create_tocs_from_high_dimension_list(self, lst_tocs : list):
        """
        create_tocs_from_high_dimension_list creates the table of contents from a
        multi-dimension list.
        """
        self.hex_current_layer_index = 0x00000000
        self.int_current_layer_pointer = 0
        self.dict_tocs = {}
        self.__creat_sublayer_from_list(lst_tocs)
    def create_tocs_from_text_list(self, lst_text : list):
        """
        create_tocs_from_console creats the table of contents from
        multiple-line inputs from the console.
        """
        self.hex_current_layer_index = 0x00000000
        self.int_current_layer_pointer = 0
        self.dict_tocs = {}
        for iter_item in lst_text:
            if 1 <= iter_item.count('\t') + 1 <= 8:
                self.int_current_layer_pointer = iter_item.count('\t') + 1
            else:
                GeneralErrorMessage("Variable int_current_layer_pointer overflow.")
            self.__add_section(iter_item.replace('\t', ''))
    def show_tocs(self):
        """
        show_tocs shows the table of contents in the console.
        """
        lst_tocs_keys = list(self.dict_tocs.keys())
        lst_tocs_keys.sort()
        if self.dict_tocs:
            print("Index No. \t Section Name")
            for iter_item in lst_tocs_keys:
                int_layer_of_item = 9 - hex(iter_item).count('0')
                str_print = hex(iter_item)[-8:] + \
                    "\t" + \
                    "\t"*int_layer_of_item + \
                    self.dict_tocs[iter_item]
                print(str_print)
        else:
            print("The table of contents is empty.")
    def return_tocs_printout(self):
        """
        return_tocs_printout returns the table of contents in a list. The
        list can be printed in the updated bib file.
        """
        if self.dict_tocs:
            lst_print = []
            lst_tocs_keys = list(self.dict_tocs.keys())
            lst_tocs_keys.sort()
            for iter_item in lst_tocs_keys:
                int_layer_of_item = 9 - hex(iter_item).count('0')
                str_print = "\t"*(int_layer_of_item-1) + \
                    self.dict_tocs[iter_item]
                lst_print.append(str_print)
            return lst_print
        return None
    def return_tocs_all_keys(self):
        """
        return_tocs_all_keys returns all the keys of the table of contents.
        """
        if self.dict_tocs:
            lst_tocs_keys = list(self.dict_tocs.keys())
            lst_tocs_keys.sort()
            return lst_tocs_keys
        return None
    def return_tocs_leaf_keys(self):
        """
        return_tocs_leaf_keys returns all the keys of the table of contents that
        do not possess any lower layer subsections.
        """
        if self.dict_tocs:
            lst_print = []
            lst_tocs_keys = list(self.dict_tocs.keys())
            lst_tocs_keys.sort()
            for iter_index, iter_item in enumerate(lst_tocs_keys):
                if iter_index == len(lst_tocs_keys) - 1:
                    lst_print.append(iter_item)
                elif hex(iter_item).count('0') <= \
                    hex(lst_tocs_keys[iter_index + 1]).count('0'):
                    lst_print.append(iter_item)
            return lst_print
        return None
    def __creat_sublayer_from_list(self, lst_single_list : list):
        """
        __read_list reads a single list and create a sub-layer accordingly.
        """
        self.__change_layer(1)
        for iter_item in lst_single_list:
            if isinstance(iter_item, list):
                self.__creat_sublayer_from_list(iter_item)
            else:
                self.__add_section(iter_item)
        self.__change_layer(-1)
    def __add_section(self, str_item_name : str):
        """
        __add_section adds a new (sub)section to the current layer
        """
        int_current_layer_section_number = self.__get_current_layer_section_number()
        if 1<= int_current_layer_section_number + 1 <= 15:
            self.hex_current_layer_index = \
                self.hex_current_layer_index + 16**(8-self.int_current_layer_pointer)
            self.hex_current_layer_index = \
                self.hex_current_layer_index - \
                (self.hex_current_layer_index % 16**(8-self.int_current_layer_pointer))
        else:
            GeneralErrorMessage("Variable int_current_layer_section_number overflow.")
        self.dict_tocs[self.hex_current_layer_index] =  str_item_name
    def __change_layer(self, int_change_layer : int):
        """
        __change_layer changes the layer of the index of the talbe of contents
        """
        if 0 <= self.int_current_layer_pointer + int_change_layer <= 8:
            self.int_current_layer_pointer = \
                self.int_current_layer_pointer + int_change_layer
        else:
            GeneralErrorMessage("Variable int_current_layer_pointer overflow.")
    def __get_current_layer_section_number(self):
        """
        __get_current_layer_section_number calculates the current layer index from
        self.hex_current_layer_index and self.int_current_layer_pointer
        """
        int_d1 = (16**(8-self.int_current_layer_pointer+1))
        int_d2 = (16**(8-self.int_current_layer_pointer))
        return (self.hex_current_layer_index % int_d1) // int_d2
