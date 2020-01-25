from pathlib import Path
from typing import Tuple

class ReadCancelledError(Exception):
    pass

def read(filename, callback=None) -> Tuple[str, str]:
    def handle_callback():
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
                    yield lines_buffer[0], ''.join(lines_buffer[1:])
                    lines_buffer.clear()

                    if handle_callback():
                        raise ReadCancelledError

                lines_buffer.append(line[1:])
            else:
                lines_buffer.append(line)

        if lines_buffer:
            yield lines_buffer[0], ''.join(lines_buffer[1:])
            if handle_callback():
                raise ReadCancelledError
