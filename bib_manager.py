# -*- coding: utf-8 -*-
"""
Class BibManager defines a ".bib" file management tool for LaTeX users. 
Class BibManager can create/open a ".bib" file, and do the followings:
(a) create/edit tree-structure table of contents;
(b) insert the table of contents into the beginning of the ".bib" file;
(c) read existing references and table of contents in the ".bib" file;
(d) insert a new reference into the ".bib" file under a tag;
(e) search/edit/remove an existing reference;
(f) sort references order in the ".bib" under their tag;
(g) global replace in title, e.g. "GUI" to "{GUI}";
(h) global replace in publisher/journal name, e.g. "System" to "Syst.";
(i) (optional) update with google scholar.
@author: sunlu.electric@gmail.com
"""

import os

class BibManager:
    """
    Class BibManager defines a ".bib" file management tool for LaTeX users.
    """
    def __init__(self):
        path_bib = input("Enter the path to the bib file (e.g.: ./refs.bib): ")
        if os.path.isfile(path_bib):
            print("The path directs to an exsiting .bib file...\n")
            str_input = input("Key in YES to confirm processing the existing .bib file.\n")
            if str_input.upper() == 'YES':
                print("The path to the .bib file is confirmed.\n")
                self.path_bib = path_bib
            else:
                print("The path to the .bib file is aborted.\n")
                str_input = input("Press Enter to continue...\n")
        else:
            print("There is no .bib file found in the given path.\n")
            print("A new .bib file is created and the path is confirmed.\n")
            self.path_bib = path_bib
            f_bib = open(self.path_bib, 'w')
            f_bib.write('%% ' + self.path_bib.split('/')[-1] + ' %%' + '\n')
            f_bib.close()


