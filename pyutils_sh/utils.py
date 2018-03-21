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
        Full path to a file. Defaults to the currently executing Python file.
        
    Returns
    -------
    directory : string
        Path to the directory containing the file.
    filename : string
        Name of the file.
    """
    
    return os.path.split(f)
