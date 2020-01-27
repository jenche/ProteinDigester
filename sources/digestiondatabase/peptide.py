from typing import Optional

from .aminoacidsequence import AminoAcidSequence


class Peptide(AminoAcidSequence):
    def __init__(self, sequence: str, missed_cleavages: int, unique: bool = False, peptide_id: Optional[int] = None):
        super().__init__(sequence, sequence_id=peptide_id)
        self._missed_cleavages = missed_cleavages
        self._unique = unique

    @property
    def missed_cleavages(self) -> int:
        return self._missed_cleavages

    @property
    def unique(self) -> bool:
        return self._unique
