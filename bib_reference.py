# -*- coding: utf-8 -*-
"""
Class BibReference is a dataclass used to record a single reference information.
@author: github.com/sunluelectric
"""

from enum import Enum
from dataclasses import dataclass

class PublicationType(Enum):
    book = 1
    article = 2
    inproceedings = 3
    online = 4
    others = 5

@dataclass
class BibReference:
    """
    Class BibReference is a dataclass used to record a single reference information.
    """
    enum_type : PublicationType
    str_type : str
    str_id : str
    str_title : str
    str_author : str
    # book and article
    str_journal : str
    int_volume : int
    int_number : int
    lst_pages : list
    int_year : int
    str_publisher : str
    # inproceedings
    str_booktitle : str
    str_organization : str
    # online
    str_url : str
    str_urldate : str
    # bib management
    hex_layer_index : int
    