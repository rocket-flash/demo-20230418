#! /usr/bin/env python
import sys
from pathlib import Path
from devtools import debug

from katana_tsl_parser.models import TslModel

if len(sys.argv) != 2:
    raise ValueError(f"Usage: {sys.argv[0]} tsl-file")

tsl = TslModel.parse_file(sys.argv[1])
root = Path(__file__).parent.parent

for i, p in enumerate(tsl.data[0]):
    # (root / f"{i:02}-{p.param_set.name}.json").write_text(p.json(indent=2))
    print(f"Patch Name: {p.param_set.name}")
    print(f"Patch: {debug.format(p.param_set.patch0)}")
    print(f"Patch: {debug.format(p.param_set.patch1)}")
    print(f"Patch: {debug.format(p.param_set.patch2)}")
