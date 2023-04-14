from pydantic import BaseModel, Field, validator


class ParamSetModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    name: str = Field(alias="UserPatch%PatchName")
    patch0: list[str] = Field(alias="UserPatch%Patch_0")
    fx1: list[str] = Field(alias="UserPatch%Fx(1)")
    fx2: list[str] = Field(alias="UserPatch%Fx(2)")
    delay1: list[str] = Field(alias="UserPatch%Delay(1)")
    delay2: list[str] = Field(alias="UserPatch%Delay(2)")
    patch1: list[str] = Field(alias="UserPatch%Patch_1")
    patch2: list[str] = Field(alias="UserPatch%Patch_2")
    status: list[str] = Field(alias="UserPatch%Status")
    knob_assign: list[str] = Field(alias="UserPatch%KnobAsgn")
    expression_pedal_assign: list[str] = Field(alias="UserPatch%ExpPedalAsgn")
    expression_pedal_min_max: list[str] = Field(alias="UserPatch%ExpPedalAsgnMinMax")
    gafc_expression1_assign: list[str] = Field(alias="UserPatch%GafcExp1Asgn")
    gafc_expression1_min_max: list[str] = Field(alias="UserPatch%GafcExp1AsgnMinMax")
    gafc_expression2_assign: list[str] = Field(alias="UserPatch%GafcExp2Asgn")
    gafc_expression2_min_max: list[str] = Field(alias="UserPatch%GafcExp2AsgnMinMax")
    footswitch_assign: list[str] = Field(alias="UserPatch%FsAsgn")
    patch_mk2v2: list[str] = Field(alias="UserPatch%Patch_Mk2V2")
    contour1: list[str] = Field(alias="UserPatch%Contour(1)")
    contour2: list[str] = Field(alias="UserPatch%Contour(2)")
    contour3: list[str] = Field(alias="UserPatch%Contour(3)")
    eq2: list[str] = Field(alias="UserPatch%Eq(2)")

    @validator("name", pre=True)
    def validate_name(cls, v: str | list[str]) -> str:  # noqa: N805
        if isinstance(v, list):
            v = "".join([chr(int(i, 16)) for i in v]).strip()

        if len(v) > 16:
            raise ValueError("must be 16 chars or fewer.")

        return v


class PatchModel(BaseModel):
    memo: str
    param_set: ParamSetModel = Field(alias="paramSet")

    class Config:
        allow_population_by_field_name = True


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
