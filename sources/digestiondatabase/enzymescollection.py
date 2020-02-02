from configparser import ConfigParser, DuplicateSectionError, DuplicateOptionError
from pathlib import Path
from typing import List, Union

from .enzyme import Enzyme


class InvalidEnzymeFileError(Exception):
    pass


class InvalidEnzymeError(Exception):
    pass


_enzymes = {}


def load_from_file(filename: Union[str, Path]):
    global _enzymes
    enzyme_file = ConfigParser()
    enzymes = {}

    filepath = Path(filename)
    if not filepath.exists():
        raise FileNotFoundError

    try:
        enzyme_file.read(filename)
    except DuplicateSectionError:
        raise InvalidEnzymeFileError(f'Some enzymes have the same name.')
    except DuplicateOptionError:
        raise InvalidEnzymeFileError(f'Some enzymes have more than one rule or description.')

    for section in enzyme_file.sections():
        name = section
        try:
            rule = enzyme_file[section]['rule']
        except KeyError:
            raise InvalidEnzymeFileError(f'Missing rule for enzyme {name}.')

        try:
            description = enzyme_file[section]['description']
        except KeyError:
            raise InvalidEnzymeFileError(f'Missing description for enzyme {name}.')

        enzymes[name] = Enzyme(name, description, rule)

    _enzymes = {key: enzymes[key] for key in sorted(enzymes.keys())}


def available_enzymes() -> List[str]:
    return sorted(_enzymes.keys())


def enzyme(name: str) -> Enzyme:
    try:
        return _enzymes[name]
    except KeyError:
        raise InvalidEnzymeError
