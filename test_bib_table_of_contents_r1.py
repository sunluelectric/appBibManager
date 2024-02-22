import unittest
from bib_table_of_contents import BibTableOfContents


class BibTableOfContentsTest(unittest.TestCase):
    def test_create_tocs_from_multidimensional_list(self):
        toc = BibTableOfContents()
        toc.create_tocs_from_multidimensional_list(
            ['Introduction', ['Methods', 'Results']])
        self.assertEqual(toc.return_tocs_printout(), [
            'Introduction',
            '    Methods',
            '    Results'
        ])

    def test_create_tocs_from_space_list(self):
        toc = BibTableOfContents()
        toc.create_tocs_from_space_list([
            'Introduction',
            '    Methods',
            '    Results'
        ])
        self.assertEqual(toc.return_tocs_printout(), [
            'Introduction',
            '    Methods',
            '    Results'
        ])

    def test_display_tocs(self):
        toc = BibTableOfContents()
        toc.create_tocs_from_multidimensional_list(
            ['Introduction', ['Methods', 'Results']])
        # Redirect stdout to capture the output
        import sys
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output
        toc.display_tocs()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), '''Index No.   Section Name
10000000    Introduction
11000000        Methods
12000000        Results''')

    def test_return_tocs_all_keys(self):
        toc = BibTableOfContents()
        toc.create_tocs_from_multidimensional_list(
            ['Introduction', ['Methods', 'Results']])
        self.assertEqual(toc.return_tocs_all_keys(), [
                         int(0x10000000), int(0x11000000), int(0x12000000)])

    def test_return_tocs_leaf_keys(self):
        toc = BibTableOfContents()
        toc.create_tocs_from_multidimensional_list(
            ['Introduction', ['Methods', 'Results']])
        self.assertEqual(toc.return_tocs_leaf_keys(), [
                         int(0x11000000), int(0x12000000)])


if __name__ == '__main__':
    unittest.main()
