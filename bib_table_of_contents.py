# -*- coding: utf-8 -*-
"""
Class BibTableOfContents is a dataclass that represents the table of contents
used in class BibManager.
@sunluelectric: github.com/sunluelectric
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
        """
        Initializes a new instance of the BibTableOfContents class.
        """
        self.hex_section_index = 0x00000000
        self.int_section_layer = 0
        self.dict_tocs = {}
        
    def create_tocs_from_multidimensional_list(self, lst_tocs : list):
        """
        Creates the table of contents from a multi-dimensional list.
        
        Parameters:
            lst_tocs (list): The multi-dimensional list representing the table of contents.
        """
        self.hex_section_index = 0x00000000
        self.int_section_layer = 0
        self.dict_tocs = {}
        self.__create_sublayer_from_multidimensional_list(lst_tocs)
        
    def create_tocs_from_space_list(self, lst_text : list):
        """
        Creates the table of contents from a list of sections with 4 spaces used to describe subsection layer index.
        
        Parameters:
            lst_text (list): The list of sections with 4 spaces used to describe subsection layer index.
        """
        self.hex_section_index = 0x00000000
        self.int_section_layer = 0
        self.dict_tocs = {}
        for iter_item in lst_text:
            if 1 <= (len(iter_item) - len(iter_item.lstrip(' '))) // 4 + 1 <= 8:
                self.int_section_layer = (len(iter_item) - len(iter_item.lstrip(' '))) // 4 + 1
            else:
                GeneralErrorMessage("Variable int_section_layer overflow.")
            self.__add_section(iter_item.lstrip(' '))
            
    def display_tocs(self):
        """
        Shows the table of contents in the console.
        """
        lst_tocs_keys = list(self.dict_tocs.keys())
        lst_tocs_keys.sort()
        if self.dict_tocs:
            print("Index No.   Section Name")
            for iter_item in lst_tocs_keys:
                int_layer_of_item = 9 - hex(iter_item).count('0')
                str_print = hex(iter_item)[-8:] + "    "*int_layer_of_item + self.dict_tocs[iter_item]
                print(str_print)
        else:
            print("The table of contents is empty.")
            
    def return_tocs_printout(self):
        """
        Returns the table of contents in a list with printout format.
        
        Returns:
            list: The table of contents in a list with printout format.
        """
        if self.dict_tocs:
            lst_print = []
            lst_tocs_keys = list(self.dict_tocs.keys())
            lst_tocs_keys.sort()
            for iter_item in lst_tocs_keys:
                int_layer_of_item = 9 - hex(iter_item).count('0')
                str_print = '    '*(int_layer_of_item-1) + self.dict_tocs[iter_item]
                lst_print.append(str_print)
            return lst_print
        return None
    
    def return_tocs_all_keys(self):
        """
        Returns all section indexes.
        
        Returns:
            list: All section indexes.
        """
        if self.dict_tocs:
            lst_tocs_keys = list(self.dict_tocs.keys())
            lst_tocs_keys.sort()
            return lst_tocs_keys
        return None
    
    def return_tocs_leaf_keys(self):
        """
        Returns all the section indexes where the section does not have a subsection.
        
        Returns:
            list: All the section indexes where the section does not have a subsection.
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
    
    def __create_sublayer_from_multidimensional_list(self, lst_single_list : list):
        """
        Creates a sub-layer in the table of contents from a list in a recursive manner.
        
        Parameters:
            lst_single_list (list): The list representing the sub-layer of the table of contents.
        """
        self.__change_layer(1)
        for iter_item in lst_single_list:
            if isinstance(iter_item, list):
                self.__create_sublayer_from_multidimensional_list(iter_item)
            else:
                self.__add_section(iter_item)
        self.__change_layer(-1)
        
    def __add_section(self, str_item_name : str):
        """
        Adds a new section to the current layer.
        
        Parameters:
            str_item_name (str): The name of the section to be added.
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
        Changes int_section_layer.
        
        Parameters:
            int_change_layer (int): The amount to change the section layer by.
        """
        if 0 <= self.int_section_layer + int_change_layer <= 8:
            self.int_section_layer = self.int_section_layer + int_change_layer
        else:
            GeneralErrorMessage("Variable int_section_layer overflow.")
            
    def __get_layer_num_of_section(self):
        """
        Calculates the number of existing sections in the layer indicated by int_section_layer.
        
        Returns:
            int: The number of existing sections in the layer.
        """
        int_d1 = (16**(8-self.int_section_layer+1))
        int_d2 = (16**(8-self.int_section_layer))
        return (self.hex_section_index % int_d1) // int_d2
