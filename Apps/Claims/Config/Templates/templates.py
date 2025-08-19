from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class Claim(BaseModel):
    report_type: str = Field(description="Report type, like 'Final' or 'Update' or 'Interim' or 'Full and Final' or etc.")
    msn: int = Field(description="From: *Case Number* or *Manufacturer’s Serial Number* or *MSN* or *Serial* or *SERIAL NO* or *case_id* field")
    aircraft: str = Field(description="From: *AIRCRAFT TYPE* or *Type and Model* or *Aircraft* or *TYPE* field")
    registration: str = Field(description="From: *Registration* or *Reg* or *Reg No* field")
    insured: str = Field(description="From: *Insured* field.")
    insurer: str = Field(description="From: *LEAD INSURER* or *INSURERS* or *To* field")
    cause: str = Field(description="From: *Incident* or *CIRCUMSTANCES/CAUSE* or *DAMAGE/LOSS* or *CIRCUMSTANCES* field")
    location: str = Field(description="From: *LOCATION OF LOSS* or *INCIDENT LOCATION* or *Incident* field")
    dol: date = Field( description="From: *Date of Loss* or *DATE OF LOSS* or *INCIDENT DATE* field.")
    indemnity_reserve: float = Field(description="""From: *LOSS RESERVE* or *CLAIMED AMOUNT* or *Indemnity Reserve* field""")
    indemnity_reserve_currency: str = Field(description="From: *LOSS RESERVE* or *CLAIMED AMOUNT* or *Indemnity Reserve* field")
    paid_to_date: float = Field(description="From: *Paid to Date* field")
    paid_to_date_currency: str = Field(description="From: *Paid to Date* field")

    summary: str = Field(description="""From: *Claim Update* or *EXECUTIVE SUMMARY* or *Summary* field""")

    contact_name: str = Field(description="From: end of last page")
    contact_title: str = Field(description="From: end of last page")
    contact_phone: str = Field(description="From: end of last page")
    contact_email: str = Field(description="From: end of last page")