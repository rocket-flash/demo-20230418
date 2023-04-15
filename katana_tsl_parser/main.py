#! /usr/bin/env python
import sys
from pathlib import Path

from katana_tsl_parser.models import AmpType, TslModel

x = AmpType(8)
print(x)

if len(sys.argv) != 2:
    raise ValueError(f"Usage: {sys.argv[0]} tsl-file")

tsl = TslModel.parse_file(sys.argv[1])
root = Path(__file__).parent.parent

for i, p in enumerate(tsl.data[0]):
    (root / f"{i:02}-{p.param_set.name}.json").write_text(p.json(indent=2))
    print(p.param_set)
    # print(f"{p.param_set.name}: {p.param_set.patch0[17]}")
