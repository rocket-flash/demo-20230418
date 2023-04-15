from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, validator

JsonDict = dict[str, Any]


def i(n: str) -> int:
    return int(n, 16)


class TslBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True


class AmpType(Enum):
    # Official
    Acoustic = 0x01
    Clean = 0x08
    Crunch = 0x0B
    Lead = 0x18
    Brown = 0x17
    # Variations
    AcousticVar = 0x1C
    CleanVar = 0x1D
    CrunchVar = 0x1E
    LeadVar = 0x1F
    BrownVar = 0x20
    # "Sneaky Amps"
    NaturalClean = 0x00
    CleanTwin = 0x09
    ComboCrunch = 0x02
    ProCrunch = 0x0A
    DeluxeCrunch = 0x0C
    StackCrunch = 0x03
    VODrive = 0x0D
    BGDrive = 0x11
    MatchDrive = 0x0F
    PowerDrive = 0x05
    VOLead = 0x0E
    BGLead = 0x10
    ExtremeLead = 0x06
    TAmpLead = 0x16
    MS1959I = 0x12
    MS1959I_II = 0x13
    HiGainStack = 0x04
    RFierVintage = 0x14
    RFierModern = 0x15
    CoreMetal = 0x07
    Custom = 0x19


class Patch0Model(TslBaseModel):
    amp_type: AmpType
    gain: int
    volume: int
    raw: list[str]

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 72:
            raise ValueError("must contain exactly 72 items")

        res = {
            "amp_type": AmpType(i(values[17])),
            "gain": i(values[18]),
            "volume": i(values[24]),
            "raw": values,
        }

        return res


class ParamSetModel(TslBaseModel):
    name: str = Field(alias="UserPatch%PatchName")
    patch0: Patch0Model = Field(alias="UserPatch%Patch_0")

    # fx1: list[str] = Field(alias="UserPatch%Fx(1)")
    # fx2: list[str] = Field(alias="UserPatch%Fx(2)")
    # delay1: list[str] = Field(alias="UserPatch%Delay(1)")
    # delay2: list[str] = Field(alias="UserPatch%Delay(2)")
    # patch1: list[str] = Field(alias="UserPatch%Patch_1")
    # patch2: list[str] = Field(alias="UserPatch%Patch_2")
    # status: list[str] = Field(alias="UserPatch%Status")
    # knob_assign: list[str] = Field(alias="UserPatch%KnobAsgn")
    # expression_pedal_assign: list[str] = Field(alias="UserPatch%ExpPedalAsgn")
    # expression_pedal_min_max: list[str] = Field(alias="UserPatch%ExpPedalAsgnMinMax")
    # gafc_expression1_assign: list[str] = Field(alias="UserPatch%GafcExp1Asgn")
    # gafc_expression1_min_max: list[str] = Field(alias="UserPatch%GafcExp1AsgnMinMax")
    # gafc_expression2_assign: list[str] = Field(alias="UserPatch%GafcExp2Asgn")
    # gafc_expression2_min_max: list[str] = Field(alias="UserPatch%GafcExp2AsgnMinMax")
    # footswitch_assign: list[str] | None = Field(alias="UserPatch%FsAsgn")
    # patch_mk2v2: list[str] | None = Field(alias="UserPatch%Patch_Mk2V2")
    # contour1: list[str] | None = Field(alias="UserPatch%Contour(1)")
    # contour2: list[str] | None = Field(alias="UserPatch%Contour(2)")
    # contour3: list[str] | None = Field(alias="UserPatch%Contour(3)")
    # eq2: list[str] | None = Field(alias="UserPatch%Eq(2)")

    @validator("name", pre=True)
    def validate_name(cls, v: str | list[str]) -> str:  # noqa: N805
        if isinstance(v, list):
            v = "".join([chr(int(i, 16)) for i in v])

        if len(v) > 16:
            raise ValueError("must be 16 chars or fewer")

        return v.rstrip()

    @validator("patch0", pre=True)
    def parse_patch0(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return Patch0Model.decode(v)


class MemoModel(TslBaseModel):
    memo: str
    is_tone_central_patch: bool = Field(alias="isToneCentralPatch")
    note: str


class PatchModel(TslBaseModel):
    memo: str | MemoModel
    param_set: ParamSetModel = Field(alias="paramSet")


class TslModel(TslBaseModel):
    name: str
    format_rev: str = Field(alias="formatRev")
    device: str
    data: list[list[PatchModel]]

    @validator("device")
    def validate_device(cls, v: str) -> str:  # noqa: N805
        if v != "KATANA MkII":
            raise ValueError(f"Unsupported device: {v}")

        return v
