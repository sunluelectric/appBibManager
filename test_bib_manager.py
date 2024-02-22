import unittest
from unittest.mock import patch
from bib_manager import BibManager


class BibManagerTest(unittest.TestCase):
    def setUp(self):
        self.bib_manager = BibManager()

    def test_set_path(self):
        self.bib_manager.set_path('/path/to/bib_file.bib')
        self.assertEqual(self.bib_manager.path_bib, '/path/to/bib_file.bib')

    def test_set_path_from_console_existing_file(self):
        with patch('builtins.input', return_value='/path/to/existing_bib_file.bib'):
            self.bib_manager.set_path_from_console()
        self.assertEqual(self.bib_manager.path_bib,
                         '/path/to/existing_bib_file.bib')

    def test_set_path_from_console_new_file(self):
        with patch('builtins.input', return_value='/path/to/new_bib_file.bib'):
            self.bib_manager.set_path_from_console()
        self.assertEqual(self.bib_manager.path_bib,
                         '/path/to/new_bib_file.bib')

    def test_read_bib(self):
        self.bib_manager.path_bib = '/path/to/bib_file.bib'
        with patch('bib_manager.BibManager.__read_tocs_from_bib') as mock_read_tocs, \
                patch('bib_manager.BibManager.__add_refs_from_bib') as mock_add_refs:
            self.bib_manager.read_bib()
        mock_read_tocs.assert_called_once()
        mock_add_refs.assert_called_once()

    def test_update_tocs_from_console(self):
        with patch('builtins.input', side_effect=['Introduction', '    Methods', '    Results', '']):
            self.bib_manager.update_tocs_from_console()
        expected_tocs = ['Introduction', ['Methods', 'Results']]
        self.assertEqual(
            self.bib_manager.obj_tocs.return_tocs_printout(), expected_tocs)

    def test_add_refs_from_console(self):
        with patch('builtins.input', side_effect=['Ref 1', 'Ref 2', '']):
            self.bib_manager.add_refs_from_console()
        expected_refs = {'Ref 1': {}, 'Ref 2': {}}
        self.assertEqual(self.bib_manager.dict_refs, expected_refs)

    def test_update_catid_single_id(self):
        self.bib_manager.dict_refs = {
            'Ref 1': {'hex_catid': None}, 'Ref 2': {'hex_catid': None}}
        self.bib_manager.update_catid('Ref 1')
        self.assertEqual(
            self.bib_manager.dict_refs['Ref 1']['hex_catid'], 0x10000000)

    def test_update_catid_multiple_ids(self):
        self.bib_manager.dict_refs = {
            'Ref 1': {'hex_catid': None}, 'Ref 2': {'hex_catid': None}}
        self.bib_manager.update_catid(['Ref 1', 'Ref 2'])
        self.assertEqual(
            self.bib_manager.dict_refs['Ref 1']['hex_catid'], 0x10000000)
        self.assertEqual(
            self.bib_manager.dict_refs['Ref 2']['hex_catid'], 0x10000000)

    def test_update_dict_refs_categorized(self):
        self.bib_manager.obj_tocs.create_tocs_from_multidimensional_list(
            ['Introduction', ['Methods', 'Results']])
        self.bib_manager.dict_refs = {
            'Ref 1': {'hex_catid': None}, 'Ref 2': {'hex_catid': 0x10000000}}
        self.bib_manager.update_dict_refs_categorized()
        expected_categorized_refs = {
            -1: {'Ref 1': {'hex_catid': None}},
            -2: {},
            -3: {},
            0x10000000: {'Ref 2': {'hex_catid': 0x10000000}}
        }
        self.assertEqual(self.bib_manager.dict_refs_categorized,
                         expected_categorized_refs)

    def test_update_bib(self):
        self.bib_manager.path_bib = '/path/to/bib_file.bib'
        with patch('builtins.input', return_value='y'), \
                patch('bib_manager.BibManager.update_dict_refs_categorized'), \
                patch('builtins.open', create=True) as mock_open:
            self.bib_manager.update_bib()
        mock_open.assert_called_once_with('/path/to/bib_file.bib', 'w')
        mock_open.return_value.__enter__.return_value.write.assert_called()


if __name__ == '__main__':
    unittest.main()
