# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:31:34 2020

@author: u30l
"""
import os
from pathlib import Path

src_pth = os.path.dirname(__file__)

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

project_path = get_project_root() 

# from https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
def tree(dir_path: Path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """      
    # prefix components:
    space =  '    '
    branch = '│   '
    # pointers:
    tee =    '├── '
    last =   '└── '
    
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir(): # extend the prefix and recurse:
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension)
# %%            
def print_tree(project_path=project_path):
    for line in tree(project_path):
        print(line)
    return