""" https://adventofcode.com/2022/day/7 """

import re

TOTAL_SPACE = 70000000
FREE_REQUIRED = 30000000
free_needed = 0

class Node:
    def __init__(self, parent, name, isdir, size=None):
        self.parent = parent
        self.name = name
        self.isdir = isdir
        self.size = size

        if self.isdir:
            self.child_dirs = {}
            self.child_files = {}


def cd(cwd, ln):
    r = re.match(r'cd (.+)', ln)
    dirname = r.group(1)

    if dirname == '..':
        assert cwd.parent
        cwd = cwd.parent
        return cwd

    return cwd.child_dirs[dirname]


def lsdir(cwd, ln):
    r = re.match(r'dir (.+)', ln)
    dirname = r.group(1)

    n = cwd.child_dirs.get(dirname)
    if not n:
        n = Node(cwd, dirname, True)
        cwd.child_dirs[dirname] = n


def lsfile(cwd, ln):
    r = re.match(r'(\d+) (.+)', ln)
    filesize = int(r.group(1))
    filename = r.group(2)

    n = cwd.child_files.get(filename)

    if not n:
        n = Node(cwd, filename, False, filesize)
        cwd.child_files[filename] = n


def get_dir_size(dir):
    assert dir.isdir
    curdirsize = sum([n.size for n in dir.child_files.values()])
    totalsize = 0

    for subdir in dir.child_dirs.values():
        child_dirsize = get_dir_size(subdir)
        totalsize += child_dirsize

    return totalsize + curdirsize


def p1_compare(size):
    return size <= 100000


def p1_printresult(selected_dirs):
    print(f'Total <= 100k: {sum([get_dir_size(d) for d in selected_dirs])}')


def p2_compare(size):
    return size + free_needed >= FREE_REQUIRED


def p2_printresult(selected_dirs):
    smallest = min(selected_dirs, key=lambda x: get_dir_size(x))
    print(f'Smallest dir to delete: {smallest.name} at {get_dir_size(smallest)}')


def select_dirs(dir, fcompare, fprintresult, isroot=False):
    selected_dirs = []

    cur_size = get_dir_size(dir)
    if fcompare(cur_size):
        selected_dirs.append(dir)

    for subdirname, subdir in dir.child_dirs.items():
        selected_dirs += select_dirs(subdir, fcompare, fprintresult)

    if isroot:
        fprintresult(selected_dirs)

    return selected_dirs


with open('day7.input.txt') as f:
    cwd = root = None
    for ln in f:
        ln = ln.lstrip('$').strip()

        if not cwd:
            cwd = root = Node(None, '/', True)
            continue

        if ln.startswith('cd'):
            cwd = cd(cwd, ln)
        elif ln.startswith('dir'):
            lsdir(cwd, ln)
        elif ln[0].isdigit():
            lsfile(cwd, ln)

    free_needed = TOTAL_SPACE - get_dir_size(root)

select_dirs(root, p1_compare, p1_printresult, True)
select_dirs(root, p2_compare, p2_printresult, True)