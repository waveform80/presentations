#!/usr/bin/env python3

import xmlrpc.client

# PyPI classifiers for all Python 3 versions
PY3 = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.0",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
]

# PyPI classifiers for all Python 2 versions
PY2 = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.3",
]

def main():
    client = xmlrpc.client.ServerProxy('http://pypi.python.org/pypi')
    # name[0] is package name
    # name[1] is package version
    py3names = {
        name[0] for classifier in PY3 for name in client.browse([classifier])
        }
    py2names = {
        name[0] for classifier in PY2 for name in client.browse([classifier])
        }
    print("""\
Total:     {total}
Py2 only:  {py2only}
Py3 only:  {py3only}
Py2 or 3:  {both}
""".format(
    total=len(py3names | py2names),
    py2only=len(py2names - py3names),
    py3only=len(py3names - py2names),
    both=len(py2names & py3names)))

if __name__ == "__main__":
    main()
