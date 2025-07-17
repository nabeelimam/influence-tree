from typing import List, Optional
from pydantic import BaseModel, Field

class Musician(BaseModel):
    name: str = Field(..., description="The name of the musician")
    yob: int = Field(..., description="The year the musician was born")
    yod: Optional[int] = Field(None, description="The year the musician died")
    affiliations: List[str] = Field(None, description="The bands/groups the musician was a member of")
    instruments: List[str] = Field(..., description="The instrument(s) the musician plays")
    genres: List[str] = Field(..., description="The genre(s) the musician plays")
    influences: List[str] = Field(..., description="The musicians that influenced this musician, including solo artists and bands. List out all the artists, and do not include genres or movements, or vague names such as 'Motown artists' or 'Skiffle music'.")
