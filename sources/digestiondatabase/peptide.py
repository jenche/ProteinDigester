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

from typing import Optional

from .aminoacidsequence import AminoAcidSequence


class Peptide(AminoAcidSequence):
    def __init__(self,
                 sequence: str,
                 missed_cleavages: int,
                 digest_unique: bool = False,
                 sequence_unique: bool = False,
                 peptide_id: Optional[int] = None):
        super().__init__(sequence, sequence_id=peptide_id)
        self._missed_cleavages = missed_cleavages
        self._digest_unique = digest_unique
        self._sequence_unique = sequence_unique

    @property
    def missed_cleavages(self) -> int:
        return self._missed_cleavages

    @property
    def digest_unique(self) -> bool:
        return self._digest_unique

    @property
    def sequence_unique(self) -> bool:
        return self._sequence_unique
