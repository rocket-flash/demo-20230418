import sys

from katana_tsl_parser.models import TslModel

if len(sys.argv) != 2:
    raise ValueError(f"Usage: {sys.argv[0]} tsl-file")

tsl = TslModel.parse_file(sys.argv[1])
print(tsl)
