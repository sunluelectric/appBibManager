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
    dict_talbe_of_contents : dict
    def __init__(self):
        self.hex_current_layer_index = 0x00000000
        self.int_current_layer_pointer = 0
        self.dict_table_of_contents = {}
    def create_table_of_contents_from_list(self, lst_table_of_contents : list):
        """
        create_table_of_contents_from_list creates the table of contents from a
        multi-dimention list.
        """
        self.hex_current_layer_index = 0x00000000
        self.int_current_layer_pointer = 0
        self.dict_table_of_contents = {}
        self.__creat_sublayer_from_list(lst_table_of_contents)
    def create_table_of_contents_from_console(self):
        """
        create_table_of_contents_from_console creats the table of contents from
        multiple-line inputs from the console.
        """
        self.hex_current_layer_index = 0x00000000
        self.int_current_layer_pointer = 0
        self.dict_table_of_contents = {}
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
        for iter_item in lst_console_inputs:
            if 1 <= iter_item.count('\t') + 1 <= 8:
                self.int_current_layer_pointer = iter_item.count('\t') + 1
            else:
                GeneralErrorMessage("Variable int_current_layer_pointer overflow.")
            self.__add_item(iter_item.replace('\t', ''))
    def show_table_of_contents(self):
        """
        show_table_of_contents shows the table of contents in the console.
        """
        lst_table_of_contents_keys = list(self.dict_table_of_contents.keys())
        lst_table_of_contents_keys.sort()
        if self.dict_table_of_contents:
            print("The table of contents is as follows. ")
            print("Index No. \t Section Name")
            for iter_item in lst_table_of_contents_keys:
                int_layer_of_item = 9 - hex(iter_item).count('0')
                str_print = hex(iter_item)[-8:] + \
                    "\t" + \
                    "\t"*int_layer_of_item + \
                    self.dict_table_of_contents[iter_item]
                print(str_print)
        else:
            print("The table of contents has not been defined or is empty.")
    def return_table_of_contents(self):
        """
        return_table_of_contents returns the table of contents in a list. The
        list can be printed in the updated bib file.
        """
        lst_print = []
        lst_table_of_contents_keys = list(self.dict_table_of_contents.keys())
        lst_table_of_contents_keys.sort()
        if self.dict_table_of_contents:
            for iter_item in lst_table_of_contents_keys:
                int_layer_of_item = 9 - hex(iter_item).count('0')
                str_print = "\t"*(int_layer_of_item-1) + \
                    self.dict_table_of_contents[iter_item]
                lst_print.append(str_print)
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
                self.__add_item(iter_item)
        self.__change_layer(-1)
    def __add_item(self, str_item_name : str):
        """
        ____add_item adds a new (sub)section to the current layer
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
        self.dict_table_of_contents[self.hex_current_layer_index] =  str_item_name
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
