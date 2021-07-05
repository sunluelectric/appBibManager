# -*- coding: utf-8 -*-
"""
Class BibTableOfContents is a dataclass use to contain the metadata for
table of contents information used in class BibManager.
@author: sunlu
"""

from dataclasses import dataclass

@dataclass
class BibTableOfContents:
    """
    Class BibTableOfContents is a dataclass use to contain the metadata for
    table of contents information used in class BibManager.
    """
    hex_table_of_contents_index : int
    int_layer_pointer : int
    dict_talbe_of_contents : dict
    def __init__(self):
        self.hex_table_of_contents_index = 0x00000000
        self.int_layer_pointer = 0
        self.dict_table_of_contents = {}
    def add_item(self, str_item_name : str):
        """
        __add_item adds a new (sub)section to the current layer
        """
        # hex index add 1 to the current layer
        # hex index clear zero for rest digits
        # self.hex_table_of_contents_index = ? 2^^int_layer_pointer
        self.dict_talbe_of_contents[self.hex_table_of_contents_index] =  str_item_name
    def change_layer(self, int_change_layer : int):
        """
        change_layer changes the layer of the index of the talbe of contents
        """
        self.int_layer_pointer = self.int_layer_pointer + int_change_layer
