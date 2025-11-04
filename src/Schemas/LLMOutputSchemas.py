from typing import Optional, Any, List

from pydantic import BaseModel, Field
from .Enums.Enums import FileTypeEnum


class ReasonSchema(BaseModel):
    confidence: float = Field(..., description="The probability level of the selected type of document being examined. If document not defined = 0.0", lt=1.1, gt=-0.1)
    reason: str = Field(..., description="Short brief explanation why this type was chosen")


class FileTypeSchema(ReasonSchema):
    document_type: FileTypeEnum = Field(default=FileTypeEnum.NOT_DEFINED, description="Type of document being examined")


class PageNavigationSchema(ReasonSchema):
    page_navigation: bool = Field(..., description="Is page navigation in")
    pages: None | str = Field(..., description="Pages range where page navigation in. From 2 to ..., but if not = None")


class DefaultMessageSchema(BaseModel):
    output: str | int | dict | list[dict | str| int] = Field(..., description="The output message")


class FoundedFieldSchema(ReasonSchema):
    field: str = Field(..., description="Field of the document being examined")
    value: str | int | float | None = Field(..., description="Value of the field being examined")


class FoundedFieldsSchema(BaseModel):
    data: list[FoundedFieldSchema] = Field(..., description="List of fields founded")


class FieldExtractionResult(ReasonSchema):
    field: str = Field(..., description="Field name we searched for")
    value: Optional[str | int | float] = Field(None, description="Found value (str, int, float)")
    auto_added_synonyms: List[str] = Field(default_factory=list, description="Synonyms automatically proposed by LLM")


class LeaseAgreementData(BaseModel):
    aircraft_count: Optional[int] = Field(None, description="Number of aircraft in the lease")
    engines_count: Optional[int] = Field(None, description="Number of engines in the lease")
    aircraft_type: Optional[str] = Field(None, description="Aircraft type, e.g., A320, B737")
    msn: Optional[str] = Field(None, description="Main aircraft MSN")
    engines_manufacturer: Optional[str] = Field(None, description="Manufacturer of the engines")
    engines_models: Optional[str] = Field(None, description="Model(s) of engines")
    engine1_msn: Optional[str] = Field(None, description="First engine MSN")
    engine2_msn: Optional[str] = Field(None, description="Second engine MSN")
    aircraft_registration: Optional[str] = Field(None, description="Aircraft registration number")
    dated: Optional[str] = Field(None, description="Date of the agreement")
    lessee: Optional[str] = Field(None, description="Lessee company name")
    lessor: Optional[str] = Field(None, description="Lessor company name")
    currency: Optional[str] = Field(None, description="Currency of contract")
    damage_proceeds_threshold: Optional[str] = Field(None, description="Damage proceeds threshold")
    aircraft_agreed_value: Optional[str] = Field(None, description="Agreed value of aircraft")
    aircraft_hull_all_risks: Optional[str] = Field(None, description="Insurance type: Hull All Risks")
    min_liability_coverages: Optional[str] = Field(None, description="Minimum liability coverages required")
    all_risks_deductible: Optional[str] = Field(None, description="All Risks deductible amount")



__all__ = [
    "FileTypeSchema", "PageNavigationSchema", "DefaultMessageSchema", "FoundedFieldSchema", "LeaseAgreementData",
    "FieldExtractionResult"
]
