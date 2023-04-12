import sys

from pydantic import BaseModel, Field, validator


class ParamSetModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    name: str = Field(alias="UserPatch%PatchName")

    @validator("name", pre=True)
    def validate_name(cls, v: list[str]) -> str:  # noqa: N805
        return "".join([chr(int(i, 16)) for i in v]).strip()


class PatchModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    memo: str
    param_set: ParamSetModel = Field(alias="paramSet")


class TslModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    name: str
    format_rev: str = Field(alias="formatRev")
    device: str
    data: list[list[PatchModel]]

    @validator("device")
    def validate_device(cls, v: str) -> str:  # noqa: N805
        if v != "KATANA MkII":
            raise ValueError(f"Unsupported device: {v}")

        return v


if len(sys.argv) != 2:
    raise ValueError(f"Usage: {sys.argv[0]} tsl-file")

tsl = TslModel.parse_file(sys.argv[1])

print(tsl)
