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

from pathlib import Path
from typing import Iterator, Optional, Callable, Union

from .protein import Protein


class ReadCancelledError(Exception):
    pass


def read(filename: Union[Path, str], callback: Optional[Callable] = None) -> Iterator[Protein]:
    def handle_callback() -> bool:
        if callback:
            return callback(position, filesize)
        else:
            return False

    filepath = Path(filename)
    if not filepath.exists():
        raise FileNotFoundError

    lines_buffer = []
    filesize = filepath.stat().st_size
    position = 0
    handle_callback()

    with open(filename, 'r') as file:
        for line in file:
            position += len(line)
            line = line.strip()

            if not line:
                continue

            if line[0] == '>':
                if lines_buffer:
                    yield Protein(lines_buffer[0], ''.join(lines_buffer[1:]))
                    lines_buffer.clear()

                    if handle_callback():
                        raise ReadCancelledError

                lines_buffer.append(line[1:])
            else:
                lines_buffer.append(line)

        if lines_buffer:
            yield Protein(lines_buffer[0], ''.join(lines_buffer[1:]))

            if handle_callback():
                raise ReadCancelledError
