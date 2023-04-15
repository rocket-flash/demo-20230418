#! /usr/bin/env python
import sys
import json
from copy import deepcopy
from pathlib import Path
from devtools import debug

from katana_tsl_parser.models import TslModel, AmpType

root = Path(__file__).parent.parent

if len(sys.argv) != 2:
    raise ValueError(f"Usage: {sys.argv[0]} tsl-file")


def print_file_content(f):
    tsl = TslModel.parse_file(f)

    for d in tsl.data:
        for _, p in enumerate(d):
            # (root / f"{i:02}-{p.param_set.name}.json").write_text(p.json(indent=2))
            print(f"Patch: {debug.format(p.param_set)}")


def encode_name(name):
    if len(name) > 16:
        raise ValueError("Name too long")

    return [f"{ord(c):02x}" for c in name] + ["20"] * (16 - len(name))


def s(v):
    return f"{v:02x}"


def update_some_values(f):
    tsl = json.loads(Path(f).read_text())

    default_patch = tsl["data"][0][0]
    for v in (0, 1, 5, 10, 20, 42, 55, 100):
        patch = deepcopy(default_patch)

        val = s(v)
        patch["paramSet"]["UserPatch%PatchName"] = encode_name(f"Patch0[25]-{v:02}")
        patch["paramSet"]["UserPatch%Patch_0"][20] = val
        patch["paramSet"]["UserPatch%Patch_0"][21] = val
        patch["paramSet"]["UserPatch%Patch_0"][22] = val

        patch["paramSet"]["UserPatch%Patch_0"][25] = val

        tsl["data"][0].append(patch)

    Path("patches.tsl").write_text(json.dumps(tsl))


# update_some_values(sys.argv[1])
print_file_content(sys.argv[1])
