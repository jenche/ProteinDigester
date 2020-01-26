import re
from typing import Tuple, List


class InvalidEnzymeError(Exception):
    pass


_enzymes = {
    'Arg-C': re.compile(r'R'),
    'Asp-C': re.compile(r'\w(?=[BD])'),
    'Asp-N_ambic': re.compile(r'\w(?=[DE])'),
    'Chymotrypsin': re.compile(r'([FLYW](?=[^P]))'),
    'CNbr': re.compile(r'M'),
    'CNbr+Trypsin': re.compile(r'(M)|([KR](?=[^P]))'),
    'Formic acid': re.compile(r'D'),
    'Lys-C': re.compile(r'K(?=[^P])'),
    'Lys-C/P': re.compile(r'K'),
    'Lys-N': re.compile(r'\w(?=K)'),
    'Trypsin': re.compile(r'[KR](?=[^P])'),
    'Trypsin/P': re.compile(r'[KR]'),
    'TrypChymo': re.compile(r'[FLWYKR](?=[^P])')
}


def available_enzymes() -> List[str]:
    return sorted(_enzymes.keys())


def cleave(sequence: str, enzyme: str, missed_cleavages: int) -> Tuple[Tuple[str, int]]:
    try:
        regexp = _enzymes[enzyme]
    except KeyError:
        raise InvalidEnzymeError

    cleavage_sites = [0] + [match.end() for match in regexp.finditer(sequence)] + [len(sequence)]
    peptides = tuple(sequence[cleavage_sites[i]:cleavage_sites[i + 1]] for i in range(0, len(cleavage_sites) - 1))

    if not missed_cleavages:
        return tuple((peptide, 0) for peptide in peptides)

    return tuple((''.join(peptides[i:j]), j - i - 1) for i in range(len(peptides)) for j in
                 range(i + 1, min(i + missed_cleavages + 2, len(peptides) + 1)))
