# -*- coding: utf-8 -*-
"""
Class BibTableOfContents is a dataclass that represents the table of contents
used in class BibManager.
@author: github.com/sunluelectric
"""

from dataclasses import dataclass
from self_error import GeneralErrorMessage

@dataclass
class BibTableOfContents:
    """
    Class BibTableOfContents is a dataclass that represents the table of contents
    used in class BibManager.
    """
    hex_section_index : int
    int_section_layer : int
    dict_tocs : dict # key: section index, value: section name
    def __init__(self):
        self.hex_section_index = 0x00000000
        self.int_section_layer = 0
        self.dict_tocs = {}
    def create_tocs_from_multidimensional_list(self, lst_tocs : list):
        """
        create_tocs_from_multidimensional_list creates the table of contents from a
        multi-dimension list.
        """
        self.hex_section_index = 0x00000000
        self.int_section_layer = 0
        self.dict_tocs = {}
        self.__creat_sublayer_from_multidimensional_list(lst_tocs)
    def create_tocs_from_tab_list(self, lst_text : list):
        """
        create_tocs_from_tab_list creats the table of contents from a list of sections
        with tab used to describe subsection layer index.
        """
        self.hex_section_index = 0x00000000
        self.int_section_layer = 0
        self.dict_tocs = {}
        for iter_item in lst_text:
            if 1 <= iter_item.count('\t') + 1 <= 8:
                self.int_section_layer = iter_item.count('\t') + 1
            else:
                GeneralErrorMessage("Variable int_section_layer overflow.")
            self.__add_section(iter_item.replace('\t', ''))
    def display_tocs(self):
        """
        display_tocs shows the table of contents in the console.
        """
        lst_tocs_keys = list(self.dict_tocs.keys())
        lst_tocs_keys.sort()
        if self.dict_tocs:
            print("Index No. \t Section Name")
            for iter_item in lst_tocs_keys:
                int_layer_of_item = 9 - hex(iter_item).count('0')
                str_print = hex(iter_item)[-8:] + "\t"*int_layer_of_item + self.dict_tocs[iter_item]
                print(str_print)
        else:
            print("The table of contents is empty.")
    def return_tocs_printout(self):
        """
        return_tocs_printout returns the table of contents in a list with printout format.
        """
        if self.dict_tocs:
            lst_print = []
            lst_tocs_keys = list(self.dict_tocs.keys())
            lst_tocs_keys.sort()
            for iter_item in lst_tocs_keys:
                int_layer_of_item = 9 - hex(iter_item).count('0')
                str_print = "\t"*(int_layer_of_item-1) + self.dict_tocs[iter_item]
                lst_print.append(str_print)
            return lst_print
        return None
    def return_tocs_all_keys(self):
        """
        return_tocs_all_keys returns all section indexes.
        """
        if self.dict_tocs:
            lst_tocs_keys = list(self.dict_tocs.keys())
            lst_tocs_keys.sort()
            return lst_tocs_keys
        return None
    def return_tocs_leaf_keys(self):
        """
        return_tocs_leaf_keys returns all the section indexes where the section
        does not have a subsection.
        """
        if self.dict_tocs:
            lst_print = []
            lst_tocs_keys = list(self.dict_tocs.keys())
            lst_tocs_keys.sort()
            for iter_index, iter_item in enumerate(lst_tocs_keys):
                if iter_index == len(lst_tocs_keys) - 1:
                    lst_print.append(iter_item)
                elif hex(iter_item).count('0') <= hex(lst_tocs_keys[iter_index + 1]).count('0'):
                    lst_print.append(iter_item)
            return lst_print
        return None
    def __creat_sublayer_from_multidimensional_list(self, lst_single_list : list):
        """
         __creat_sublayer_from_multidimensional_list creates a sub-layer in the
         table of contents from a list in a recursive manner.
        """
        self.__change_layer(1)
        for iter_item in lst_single_list:
            if isinstance(iter_item, list):
                self.__creat_sublayer_from_multidimensional_list(iter_item)
            else:
                self.__add_section(iter_item)
        self.__change_layer(-1)
    def __add_section(self, str_item_name : str):
        """
        __add_section adds a new section to the current layer
        """
        int_layer_num_of_section = self.__get_layer_num_of_section()
        if 1<= int_layer_num_of_section + 1 <= 15:
            self.hex_section_index = self.hex_section_index + 16**(8-self.int_section_layer)
            self.hex_section_index = \
                self.hex_section_index - (self.hex_section_index % 16**(8-self.int_section_layer))
        else:
            GeneralErrorMessage("Variable int_layer_num_of_section overflow.")
        self.dict_tocs[self.hex_section_index] =  str_item_name
    def __change_layer(self, int_change_layer : int):
        """
        __change_layer changes int_section_layer
        """
        if 0 <= self.int_section_layer + int_change_layer <= 8:
            self.int_section_layer = self.int_section_layer + int_change_layer
        else:
            GeneralErrorMessage("Variable int_section_layer overflow.")
    def __get_layer_num_of_section(self):
        """
        __get_layer_num_of_section calculates the number of existing sections
        in the layer indicated by int_section_layer.
        """
        int_d1 = (16**(8-self.int_section_layer+1))
        int_d2 = (16**(8-self.int_section_layer))
        return (self.hex_section_index % int_d1) // int_d2
