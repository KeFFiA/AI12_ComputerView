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
    aircraft_count: Optional[int] = Field(None, description="Number of aircraft in the file", alias="Aircraft Count")
    engines_count: Optional[int] = Field(None, description="Number of engines in the file", alias="Engines Count")
    aircraft_type: Optional[str] = Field(None, description="Aircraft type, e.g., A320, B737", alias="Aircraft Type")
    msn: Optional[str] = Field(None, description="Main aircraft MSN", alias="MSN")
    engines_manufacturer: Optional[str] = Field(None, description="Manufacturer of the engines", alias="Engines Manufacture")
    engines_models: Optional[str] = Field(None, description="Model(s) of engines", alias="Engines Models")
    engine1_msn: Optional[str] = Field(None, description="First engine MSN", alias="Engine1 MSN")
    engine2_msn: Optional[str] = Field(None, description="Second engine MSN", alias="Engine2 MSN")
    aircraft_registration: Optional[str] = Field(None, description="Aircraft registration number", alias="Aircraft Registration")
    dated: Optional[str] = Field(None, description="Date of the agreement", alias="Dated")
    lessee: Optional[str] = Field(None, description="Lessee company name", alias="Lessee")
    lessor: Optional[str] = Field(None, description="Lessor company name", alias="Lessor")
    currency: Optional[str] = Field(None, description="Currency of contract", alias="Currency")
    damage_proceeds_threshold: Optional[str] = Field(None, description="Damage proceeds threshold", alias="Damage Proceeds Threshold")
    aircraft_agreed_value: Optional[str] = Field(None, description="Agreed value of aircraft", alias="Aircraft Agreed Value")
    aircraft_hull_all_risks: Optional[str] = Field(None, description="Insurance type: Hull All Risks", alias="Hull All Risks")
    min_liability_coverages: Optional[str] = Field(None, description="Minimum liability coverages required", alias="Minimal Liability Coverages")
    all_risks_deductible: Optional[str] = Field(None, description="All Risks deductible amount", alias="All Risks Deductible")



__all__ = [
    "FileTypeSchema", "PageNavigationSchema", "DefaultMessageSchema", "FoundedFieldSchema", "LeaseAgreementData",
    "FieldExtractionResult"
]
