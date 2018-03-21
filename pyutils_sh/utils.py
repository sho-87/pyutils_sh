"""
Utility functions for general purpose Python programming.
"""

import os
import sys


def get_path(f=sys.argv[0]):
    """
    Get path to, and name of, a file.
    
    Parameters
    ----------
    f : string, optional
        Full path to a file e.g. 'C:\Users\Simon\Desktop\file.txt'. Defaults 
        to the currently executing Python file.

    Returns
    -------
    directory : string
        Path to the directory containing the file.
    filename : float
        Name of the file.
    """
    
    return os.path.split(f)
    