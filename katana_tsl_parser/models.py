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


class DrivePedalType(Enum):
    MidBoost = 0x00
    CleanBoost = 0x01
    TrebleBoost = 0x02
    CrunchOD = 0x03
    NaturalOD = 0x04
    WarmOD = 0x05
    FatDS = 0x06
    MetalDS = 0x08
    OCTFuzz = 0x09
    BluesDrive = 0x0A
    Overdrive = 0x0B
    Tubescreamer = 0x0C
    TurboOD = 0x0D
    Distortion = 0x0E
    Rat = 0x0F
    GuVDS = 0x10
    DSTPlus = 0x11
    MetalZone = 0x12
    SixtiesFuzz = 0x13
    MuffFuzz = 0x14
    HM2 = 0x15
    MetalCore = 0x16
    CentaOD = 0x17


class Light(Enum):
    Green = 0
    Red = 1
    Yellow = 2


class Patch0Model(TslBaseModel):
    drive_pedal_on: bool
    drive_pedal_type: DrivePedalType
    drive_pedal_drive: int
    drive_pedal_bottom: int
    drive_pedal_tone: int
    drive_pedal_solo_on: bool
    drive_pedal_solo_level: int
    drive_pedal_direct_mix: int
    drive_pedal_level: int

    amp_type: AmpType
    amp_gain: int
    amp_volume: int
    amp_eq_bass: int
    amp_eq_middle: int
    amp_eq_treble: int
    amp_eq_presence: int

    _raw: list[str]

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 72:
            raise ValueError("must contain exactly 72 items")

        res = {
            "drive_pedal_on": i(values[0]) > 0,
            "drive_pedal_type": DrivePedalType(i(values[1])),
            "drive_pedal_drive": i(values[2]),
            "drive_pedal_bottom": i(values[3]) - 50,
            "drive_pedal_tone": i(values[4]) - 50,
            "drive_pedal_solo_on": i(values[5]) > 0,
            "drive_pedal_solo_level": i(values[6]),
            "drive_pedal_level": i(values[7]),
            "drive_pedal_direct_mix": i(values[8]),
            "amp_type": AmpType(i(values[17])),
            "amp_gain": i(values[18]),
            "amp_eq_bass": i(values[20]),
            "amp_eq_middle": i(values[21]),
            "amp_eq_treble": i(values[22]),
            "amp_eq_presence": i(values[23]),
            "amp_volume": i(values[24]),
            "_raw": values,
        }

        return res


class Patch1Model(TslBaseModel):
    noise_suppressor_on: bool
    noise_suppressor_threshold: int
    noise_suppressor_release: int

    _raw: list[str]

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 50:
            raise ValueError("must contain exactly 50 items")

        res = {
            "noise_suppressor_on": i(values[38]) > 0,
            "noise_suppressor_threshold": i(values[39]),
            "noise_suppressor_release": i(values[40]),
            "_raw": values,
        }

        return res


class Patch2Model(TslBaseModel):
    drive_pedal_green: DrivePedalType
    drive_pedal_red: DrivePedalType
    drive_pedal_yellow: DrivePedalType

    booster_light: Light

    _raw: list[str]

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 36:
            raise ValueError("must contain exactly 36 items")

        res = {
            "drive_pedal_green": DrivePedalType(i(values[4])),
            "drive_pedal_red": DrivePedalType(i(values[5])),
            "drive_pedal_yellow": DrivePedalType(i(values[6])),
            "booster_light": Light(i(values[25])),
            "_raw": values,
        }

        return res


class ParamSetModel(TslBaseModel):
    name: str = Field(alias="UserPatch%PatchName")
    patch0: Patch0Model = Field(alias="UserPatch%Patch_0")

    # fx1: list[str] = Field(alias="UserPatch%Fx(1)")
    # fx2: list[str] = Field(alias="UserPatch%Fx(2)")
    # delay1: list[str] = Field(alias="UserPatch%Delay(1)")
    # delay2: list[str] = Field(alias="UserPatch%Delay(2)")
    patch1: Patch1Model = Field(alias="UserPatch%Patch_1")
    patch2: Patch2Model = Field(alias="UserPatch%Patch_2")
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

    @validator("patch1", pre=True)
    def parse_patch1(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return Patch1Model.decode(v)

    @validator("patch2", pre=True)
    def parse_patch2(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return Patch2Model.decode(v)


class MemoModel(TslBaseModel):
    memo: str
    is_tone_central_patch: bool = Field(alias="isToneCentralPatch")
    note: str | None


class PatchModel(TslBaseModel):
    memo: MemoModel | str
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
