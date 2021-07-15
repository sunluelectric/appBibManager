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
    str_volume : str
    str_number : str
    str_pages : str
    str_year : str
    str_publisher : str
    # inproceedings
    str_booktitle : str
    str_organization : str
    # online
    str_url : str
    str_urldate : str
    # bib management
    hex_catid: int
    def __init__(self):
        self.enum_type = None
        self.str_type = None
        self.str_id = None
        self.str_title = None
        self.str_author = None
        # book and article
        self.str_journal = None
        self.str_volume = None
        self.str_number = None
        self.str_pages = None
        self.str_year = None
        self.str_publisher = None
        # inproceedings
        self.str_booktitle = None
        self.str_organization = None
        # online
        self.str_url = None
        self.str_urldate = None
        # bib management
        self.hex_catid = None
    