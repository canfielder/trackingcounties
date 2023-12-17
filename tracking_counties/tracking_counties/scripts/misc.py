################################################################################
# SETUP #
import os 

from pathlib import Path

################################################################################
# CODE #
def get_project_directory(
    search_directory = Path.cwd(),
    root_file = 'root.txt'
    ):
    """
    Recursively searches for a specified root file in the given directory
    and its parent directories.

    Parameters
    ----------
    search_directory : pathlib.Path, optional
        The directory to start searching for the root file. Defaults to the
        current working directory (Path.cwd()).
    root_file : str, optional
        The name of the root file to search for. Defaults to 'root.txt'.

    Returns
    -------
    pathlib.Path
        The path of the directory containing the specified root file.
        If the root file is not found in the given directory or its parent
        directories, the function recursively searches in the parent
        directory.

    Raises
    ------
    AssertionError
        If the provided `search_directory` is not a pathlib.Path object,
        if `root_file` is not a string, or if `search_directory` is not a
        valid directory path.

    Examples
    --------
    To find the project directory containing 'config.txt' starting from the
    current working directory:
    
    >>> result = get_project_directory(root_file='config.txt')
    >>> print(result)

    To find the project directory containing 'settings.txt' starting from a
    specific directory:

    >>> result = get_project_directory(Path('/path/to/start/searching'), 'settings.txt')
    >>> print(result)
    """
    # Input Validation
    assert isinstance(search_directory, Path), \
        "search_directory must be a pathlib.Path object."
    assert isinstance(root_file, str), "root_file must be a string."

    # Check if the provided search_directory is a valid path
    assert search_directory.is_dir(), \
        "search_directory must be a valid directory path."

    if root_file in os.listdir(search_directory):
        return search_directory
    
    else:
        return get_project_directory(search_directory = search_directory.parent)