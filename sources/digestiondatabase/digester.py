from typing import List

from .enzyme import Enzyme


class InvalidEnzymeError(Exception):
    pass


_enzymes = {
    # 'Arg-C': re.compile(r'R'),
    # 'Asp-C': re.compile(r'\w(?=[BD])'),
    # 'Asp-N_ambic': re.compile(r'\w(?=[DE])'),
    # 'Chymotrypsin': re.compile(r'([FLYW](?=[^P]))'),
    # 'CNbr': re.compile(r'M'),
    # 'CNbr+Trypsin': re.compile(r'(M)|([KR](?=[^P]))'),
    # 'Formic acid': re.compile(r'D'),
    # 'Lys-C': re.compile(r'K(?=[^P])'),
    # 'Lys-C/P': re.compile(r'K'),
    # 'Lys-N': re.compile(r'\w(?=K)'),
    'Trypsin': Enzyme('Trypsin', 'Cleaves next to K or R, but not before P', r'[KR](?=[^P])')
    # 'Trypsin/P': re.compile(r'[KR]'),
    # 'TrypChymo': re.compile(r'[FLWYKR](?=[^P])')
}


def available_enzymes() -> List[str]:
    return sorted(_enzymes.keys())


def enzyme(name: str) -> Enzyme:
    try:
        return _enzymes[name]
    except KeyError:
        raise InvalidEnzymeError
