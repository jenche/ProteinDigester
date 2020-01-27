from typing import Optional

from .aminoacidsequence import AminoAcidSequence


class Protein(AminoAcidSequence):
    def __init__(self, name: str, sequence: str, protein_id: Optional[int] = None):
        super().__init__(sequence, sequence_id=protein_id)
        self._name = name

    @property
    def name(self) -> str:
        return self._name
