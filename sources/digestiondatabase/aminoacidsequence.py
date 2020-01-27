from typing import Optional


class AminoAcidSequence:
    def __init__(self, sequence: str, sequence_id: Optional[int] = None):
        self._id = sequence_id
        self._sequence = sequence

    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def sequence(self) -> str:
        return self._sequence
