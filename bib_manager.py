# -*- coding: utf-8 -*-
"""
Class BibManager defines a ".bib" file management tool for LaTeX users. 
Class BibManager can create/open a ".bib" file, and do the followings:
(a) create/edit tree-structure table of contents;
(b) insert the table of contents into the beginning of the ".bib" file;
(c) insert a new reference into the ".bib" file under a tag;
(d) search/edit/remove an existing reference;
(e) sort references order in the ".bib" under their tag;
(f) global replace in title, e.g. "GUI" to "{GUI}";
(g) global replace in publisher/journal name, e.g. "System" to "Syst.";
(h) (optional) update with google scholar.
@author: sunlu.electric@gmail.com
"""
