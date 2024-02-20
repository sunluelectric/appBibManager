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
    GeneralWarnningMessage is a class that prints warning messages.
    """
    @staticmethod
    def print_warning_message(*args):
        """
        print_warning_message prints the warning message.

        Args:
            *args: Variable number of arguments representing the warning message.

        Returns:
            None
        """
        if len(args)>0:
            print("Warning: +" + args[0] + "\n")
        else:
            print("Warning: A warning is raised by GeneralWarnningMessage.\n")

class VariableDebugger():
    """
    VariableDebugger prints the variable name and value.
    """
    @staticmethod
    def print_variable(var_dict):
        """
        print_variable prints the variable name and value.
        """
        for var_name, var_value in var_dict.items():
            print("Debug: " + var_name + " = " + str(var_value) + "\n")
