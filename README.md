# appBibManager

appBibManager is a Python-based tool designed to simplify the management of ".bib" files for LaTeX users. It provides a range of features to help you organize, update, and manipulate your BibTeX references.

## Features

- **Reference Management**: The `bib_manager.py` module provides functions to categorize and manage your BibTeX references. It uses the `dict_refs_categorized` dictionary to store categorized references.

- **Table of Contents Management**: The `bib_table_of_contents.py` module allows you to create and manage a table of contents for your BibTeX file. It uses the `dict_tocs` dictionary to store the table of contents.

- **Error Handling**: The `self_error.py` module contains the `GeneralWarnningMessage` class for handling and displaying warning messages.

## Usage

To use appBibManager, you can run the `bib_manager.py` script from your console. You can add references directly from the console using the `add_refs_from_console` function.

## Testing

Unit tests for the `bib_reference.py` module can be found in the `test_bib_reference.py` file.

## License

This project is licensed under the terms of the LICENSE file included in the repository.

Please refer to the individual module files for more detailed information on their functionality.