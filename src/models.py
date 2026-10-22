from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class DatasetDescription(BaseModel):
    Name: str = Field(..., description="Name of the neuroimaging dataset")
    BIDSVersion: str = Field(..., description="BIDS version, e.g., 1.8.0")
    License: Optional[str] = Field(None, description="Dataset license")
    Authors: List[str] = Field(..., description="List of dataset authors/contributors")


class ParticipantRecord(BaseModel):
    participant_id: str = Field(..., pattern=r"^sub-[a-zA-Z0-9]+$")
    age: float = Field(..., ge=0.0, le=120.0, description="Participant age in years")
    sex: str = Field(..., description="Participant biological sex")
    handedness: Optional[str] = Field(None, description="Handedness (e.g., 'right', 'left', 'mixed')")

    @field_validator("sex")
    @classmethod
    def validate_sex(cls, v: str) -> str:
        allowed = {"M", "F", "O", "male", "female", "other"}
        if v.lower() not in allowed:
            raise ValueError(f"Invalid sex value '{v}'. Must be one of {allowed}")
        return v.lower()