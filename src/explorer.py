import os


class Explorer:
    '''
    Class to recursively explore a directory and its subdirectories
    looking for .py files. Ignore directories mentioned in the ignore.

    Attributes:
    -----------
    path : str
        The path to the directory to explore
    ignore : list
        List of directories to ignore
    '''

    def __init__(self, path: str, ignore: list[str]):
        self.path = path
        self.ignore = ignore

    def explore(self) -> list[str]:
        '''
        Method to explore the directory and its subdirectories
        looking for .py files

        Returns:
        --------
        list[str]
            List of .py files found
        '''
        py_files = []
        for root, dirs, files in os.walk(self.path):
            # Remove directories to ignore
            dirs[:] = [d for d in dirs if d not in self.ignore]

            # Add .py files to the list
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))
        return py_files
