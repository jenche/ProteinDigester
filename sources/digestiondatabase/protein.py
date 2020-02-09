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


class Protein(AminoAcidSequence):
    def __init__(self, name: str, sequence: str, protein_id: Optional[int] = None):
        super().__init__(sequence, sequence_id=protein_id)
        self._name = name

    @property
    def name(self) -> str:
        return self._name
