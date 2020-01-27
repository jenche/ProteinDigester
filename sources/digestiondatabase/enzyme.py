import re
from typing import Iterator

from .aminoacidsequence import AminoAcidSequence
from .peptide import Peptide


class Enzyme:
    def __init__(self, name: str, description: str, rule: str):
        self._name = name
        self._description = description
        self._rule = re.compile(rule)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def cleave(self, aa_sequence: AminoAcidSequence, missed_cleavages: int) -> Iterator[Peptide]:
        matches = self._rule.finditer(aa_sequence.sequence)
        cleavage_sites = [0] + [match.end() for match in matches] + [len(aa_sequence.sequence)]
        digested_sequences = tuple(aa_sequence.sequence[cleavage_sites[i]:cleavage_sites[i + 1]] for i in
                                   range(len(cleavage_sites) - 1))

        # if not missed_cleavages:
        #     return (Peptide(digested_sequence, 0) for digested_sequence in digested_sequences)

        for i in range(len(digested_sequences)):
            for j in range(i + 1, min(i + missed_cleavages + 2, len(digested_sequences) + 1)):
                yield Peptide(''.join(digested_sequences[i:j]), j - i - 1)
