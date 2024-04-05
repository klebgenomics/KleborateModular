"""
Copyright 2023 Tom Stanton (tomdstanton@gmail.com)
https://github.com/klebgenomics/Kaptive

This file is part of Kaptive. Kaptive is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Kaptive is distributed
in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Kaptive.
If not, see <https://www.gnu.org/licenses/>.
"""

import os
import sys
from pathlib import Path
from typing import Generator
from gzip import open as gzopen
from pathlib import Path

from kaptive.log import log, quit_with_error, bold_cyan

# Constants -----------------------------------------------------------------------------------------------------------
_GZIP_MAGIC = b'\x1f\x8b'
_LOGO = r"""
    __               __  _           _____
   / /______ _____  / /_(_)   _____ |__  /
  / //_/ __ `/ __ \/ __/ / | / / _ \ /_ < 
 / ,< / /_/ / /_/ / /_/ /| |/ /  __/__/ / 
/_/|_|\__,_/ .___/\__/_/ |___/\___/____/  
          /_/
"""
_REVCOMP = str.maketrans('ACGTNacgtn', 'TGCANtgcan')


# Functions -----------------------------------------------------------------------------------------------------------
def check_programs(progs: list[str], verbose: bool = False):
    """Check if programs are installed and executable"""
    bins = {  # Adapted from: https://unix.stackexchange.com/a/261971/375975
        f: Path(f'{p}/{f}') for p in filter(
            os.path.isdir, os.environ["PATH"].split(os.path.pathsep)
        ) for f in os.listdir(p) if os.access(f'{p}/{f}', os.X_OK)
    }
    for program in progs:
        if program in bins.keys():
            log(f'{program}: {bins[program]}', verbose)
        else:
            quit_with_error(f'{program} not found')


def check_file(path: str | Path) -> Path:
    path = Path(path) if isinstance(path, str) else path
    if not path.exists():
        quit_with_error(f'{path.name} does not exist')
    if not path.is_file():
        quit_with_error(f'{path.name} is not a file')
    elif path.stat().st_size == 0:
        quit_with_error(f'{path.name} is empty')
    else:
        return path.absolute()



def check_cpus(cpus: int | str | None) -> int:
    if not cpus:
        return os.cpu_count()
    try:
        cpus = int(cpus)
    except ValueError:
        quit_with_error(f"CPUs must be an integer, got {cpus}")
    if cpus < 1:
        quit_with_error(f"CPUs must be > 0, got {cpus}")
    return min(cpus, os.cpu_count())


def check_dir(path: str, parents: bool = True, exist_ok: bool = True) -> Path:
    """
    Check if a directory exists, and create it if not
    """
    try:
        (path := Path(path)).mkdir(parents=parents, exist_ok=exist_ok)
        return path
    except Exception as e:
        quit_with_error(f"Could not create directory {path}: {e}")


def check_python_version(major: int = 3, minor: int = 9):
    if sys.version_info.major < major or sys.version_info.minor < minor:
        quit_with_error(f'Python version {major}.{minor} or greater required')


def is_gzipped(bytes_string: bytes) -> bool:
    """Detects gzipped byte-string"""
    return bytes_string[:2] == _GZIP_MAGIC


def find_files_with_suffixes(prefix: Path, suffixes: list[str], min_size: int = 1) -> list[Path]:
    """
    Find files with given suffixes for the given prefix, useful for finding blast database or bwa index files
    :param suffixes: List of existing Paths with suffixes
    :param prefix: Prefix as Path
    :param min_size: Minimum size of file in bytes
    :return: List[Path]
    """
    return [p for i in suffixes if
            (p := prefix.with_suffix(prefix.suffix + i)).exists() and p.stat().st_size >= min_size]


def get_logo(message: str, width: int = 43) -> str:  # 43 is the width of the logo
    return bold_cyan(f'{_LOGO}\n{message.center(width)}')


def parse_fasta(path: Path) -> Generator[tuple[str, str, str], None, None]:
    """Wrapper around fasta_parser for parsing fasta files"""
    open_func = open if path.suffix != '.gz' else gzopen
    try:  # Try to open file and parse it
        with open_func(path, 'rt') as f:
            if (first_char := (fasta_string := f.read())[0]) != '>':  # Check first character
                quit_with_error(f'First character of {path} is {first_char}, not ">"')
            yield from fasta_parser(fasta_string)
    except Exception as e:
        quit_with_error(f"Could not parse {path}: {e}, if gzipped, ensure file ends in .gz")


def fasta_parser(fasta: str) -> Generator[tuple[str, str, str], None, None]:
    """A simple fasta parser that yields a tuple of id, description, sequence for each record in a fasta file."""
    record = []
    for line in fasta.splitlines():
        if line.startswith('>'):  # New record
            if record:  # If previous record exists, yield it
                name, desc = record[0].split(' ', maxsplit=1) if ' ' in record[0] else (record[0], '')
                yield name[1:], desc,  ''.join(record[1:])  # Yield record
            record = []  # Reset record
        record.append(line)  # Add line to record
    if record:  # Yield last record
        name, desc = record[0].split(' ', maxsplit=1) if ' ' in record[0] else (record[0], '')
        yield name[1:], desc, ''.join(record[1:])  # Yield record


def reverse_complement(seq: str) -> str:
    return seq.translate(_REVCOMP)[::-1]
