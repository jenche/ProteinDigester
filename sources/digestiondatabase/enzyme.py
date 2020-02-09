#  ProteinDigester
#      Copyright (C) 2020  Julien ENCHE
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
from typing import Iterator

from .aminoacidsequence import AminoAcidSequence
from .peptide import Peptide


class InvalidRuleError(Exception):
    pass


class Enzyme:
    def __init__(self, name: str, description: str, rule: str):
        self._name = name
        self._description = description
        self._rule = rule

        try:
            self._cleave_regex = re.compile(rule)
        except re.error:
            raise InvalidRuleError

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def rule(self) -> str:
        return self._rule

    def cleave(self, aa_sequence: AminoAcidSequence, missed_cleavages: int) -> Iterator[Peptide]:
        matches = self._cleave_regex.finditer(aa_sequence.sequence)
        cleavage_sites = [0] + [match.end() for match in matches] + [len(aa_sequence.sequence)]
        digested_sequences = tuple(aa_sequence.sequence[cleavage_sites[i]:cleavage_sites[i + 1]] for i in
                                   range(len(cleavage_sites) - 1))

        for i in range(len(digested_sequences)):
            for j in range(i + 1, min(i + missed_cleavages + 2, len(digested_sequences) + 1)):
                yield Peptide(''.join(digested_sequences[i:j]), j - i - 1)
