# Python: 3.13.12 (tags/v3.13.12:1cbe481, Feb  3 2026, 18:22:25) [MSC v.1944 64 bit (AMD64)]
# Library: posixpath, version: unspecified
# Module: posixpath, version: unspecified

'Common operations on Posix pathnames.\n\nInstead of importing this module directly, import os and refer to\nthis module as os.path.  The "os.path" name is an alias for this\nmodule on Posix systems; on other systems (e.g. Windows),\nos.path provides the same operations in a manner specific to that\nplatform, and is an alias to another module (e.g. ntpath).\n\nSome of this can actually be useful on non-Posix systems too, e.g.\nfor manipulation of the pathname component of URLs.\n'

import typing
import builtins as _mod_builtins
import genericpath as _mod_genericpath

ALLOW_MISSING: _mod_genericpath.ALLOW_MISSING
__all__: list
__builtins__: dict
__doc__: str
__file__: str
__name__: str
__package__: str
def _get_sep(path) -> typing.Any:
    ...

_varpattern: str
_varsub: typing.Any
_varsubb: typing.Any
def abspath(path) -> typing.Any:
    'Return an absolute path.'
    ...

altsep: typing.Any
def basename(p) -> typing.Any:
    'Returns the final component of a pathname'
    ...

def commonpath(paths) -> typing.Any:
    'Given a sequence of path names, returns the longest common sub-path.'
    ...

def commonprefix(m) -> typing.Any:
    'Given a list of pathnames, returns the longest common leading component'
    ...

curdir: str
defpath: str
devnull: str
def dirname(p) -> typing.Any:
    'Returns the directory component of a pathname'
    ...

def exists(path) -> typing.Any:
    'Test whether a path exists.  Returns False for broken symbolic links'
    ...

def expanduser(path) -> typing.Any:
    'Expand ~ and ~user constructions.  If user or $HOME is unknown,\ndo nothing.'
    ...

def expandvars(path) -> typing.Any:
    'Expand shell variables of form $var and ${var}.  Unknown variables\nare left unchanged.'
    ...

extsep: str
def getatime(filename) -> typing.Any:
    'Return the last access time of a file, reported by os.stat().'
    ...

def getctime(filename) -> typing.Any:
    'Return the metadata change time of a file, reported by os.stat().'
    ...

def getmtime(filename) -> typing.Any:
    'Return the last modification time of a file, reported by os.stat().'
    ...

def getsize(filename) -> typing.Any:
    'Return the size of a file, reported by os.stat().'
    ...

def isabs(s) -> typing.Any:
    'Test whether a path is absolute'
    ...

def isdevdrive(path) -> typing.Any:
    'Determines whether the specified path is on a Windows Dev Drive.\nDev Drives are not supported on the current platform'
    ...

def isdir(s) -> typing.Any:
    'Return true if the pathname refers to an existing directory.'
    ...

def isfile(path) -> typing.Any:
    'Test whether a path is a regular file'
    ...

def isjunction(path) -> typing.Any:
    'Test whether a path is a junction\nJunctions are not supported on the current platform'
    ...

def islink(path) -> typing.Any:
    'Test whether a path is a symbolic link'
    ...

def ismount(path) -> typing.Any:
    'Test whether a path is a mount point'
    ...

def join(a, *p) -> typing.Any:
    "Join two or more pathname components, inserting '/' as needed.\nIf any component is an absolute path, all previous path components\nwill be discarded.  An empty last part will result in a path that\nends with a separator."
    ...

def lexists(path) -> typing.Any:
    'Test whether a path exists.  Returns True for broken symbolic links'
    ...

def normcase(s) -> typing.Any:
    'Normalize case of pathname.  Has no effect under Posix'
    ...

def normpath(path) -> typing.Any:
    'Normalize path, eliminating double slashes, etc.'
    ...

pardir: str
pathsep: str
def realpath(filename) -> typing.Any:
    'Return the canonical path of the specified filename, eliminating any\nsymbolic links encountered in the path.'
    ...

def relpath(path, start) -> typing.Any:
    'Return a relative version of a path'
    ...

def samefile(f1, f2) -> typing.Any:
    'Test whether two pathnames reference the same actual file or directory\n\nThis is determined by the device number and i-node number and\nraises an exception if an os.stat() call on either pathname fails.\n'
    ...

def sameopenfile(fp1, fp2) -> typing.Any:
    'Test whether two open file objects reference the same file'
    ...

def samestat(s1, s2) -> typing.Any:
    'Test whether two stat buffers reference the same file'
    ...

sep: str
def split(p) -> typing.Any:
    'Split a pathname.  Returns tuple "(head, tail)" where "tail" is\neverything after the final slash.  Either part may be empty.'
    ...

def splitdrive(p) -> typing.Any:
    'Split a pathname into drive and path. On Posix, drive is always\nempty.'
    ...

def splitext(p) -> typing.Any:
    'Split the extension from a pathname.\n\nExtension is everything from the last dot to the end, ignoring\nleading dots.  Returns "(root, ext)"; ext may be empty.'
    ...

def splitroot(p) -> typing.Any:
    'Split a pathname into drive, root and tail.\n\nThe tail contains anything after the root.'
    ...

supports_unicode_filenames: bool
def __getattr__(name) -> typing.Any:
    ...

