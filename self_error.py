# -*- coding: utf-8 -*-
"""
@author: sunluelectric@github
"""

class SelfDefinedError(Exception):
    """
    SelfDefinedError defines class for general error.
    """
    @staticmethod
    def print_error_message(message):
        """
        print_error_message prints the error message.
        """
        print("Error: " + message + "\n")

class GeneralErrorMessage(SelfDefinedError):
    """
    GeneralErrorMessage prints the error message and raise the error.
    """
    def __init__(self, *args):
        if len(args)>0:
            self.print_error_message(args[0])
        else:
            print("Error: An error is raised by GeneralErrorMessage.\n")

class GeneralWarnningMessage():
    """
    GeneralWarningMessage prints the warning message.
    """
    @staticmethod
    def print_warning_message(*args):
        """
        print_warning_message prints the warning message.
        """
        if len(args)>0:
            print("Warning: +" + args[0] + "\n")
        else:
            print("Warning: A warning is printed by GeneralWarningMessage.\n")
