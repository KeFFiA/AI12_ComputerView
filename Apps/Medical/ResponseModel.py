from typing import List

from pydantic import BaseModel, Field

class Insurance(BaseModel):
    CompanyName: str = Field(..., description="Company Name")
    Category: str = Field(..., description="Insurance Category")
    Number_of_Lives: int = Field(..., gt=0, description="Number of Lives")
    Area_of_Coverage_or_Geographical_Scope: str = Field(..., description="Area of Coverage or Geographical Scope")
    Extended_Territory_for_Emergency_treatment_only: str = Field(..., description="Extended Territory for Emergency treatment only")
    Annual_Aggregate_Limit: float = Field(..., gt=0, description="Annual Aggregate Limit")
    Pre_existing_conditions: str = Field(..., description="Pre-existing conditions")
    Network_Type: str = Field(..., description="Network Type")
    OP_Consultation: str = Field(..., description="Operation Consultation")
    OP_Physiotherapy: str = Field(..., description="Operation Physiotherapy")
    Pharmaceuticals: str = Field(..., description="Pharmaceuticals")
    Diagnostics: str = Field(..., description="Diagnostics")
    Dental_Benefit: str = Field(..., description="""Dental Benefit (Subject to Prior Approval) Includes: Consultation, Tooth Extraction, X-Ray (Intra Oral & Extra Oral), Root Canal Treatment (R.C.T), Amalgam / Composite Fillings, Scaling & Polishing, Crowns following a Root Canal Treatments, Anesthesia. Orthodontics Not Covered""")
    Optical_Benefit: str = Field(..., description="""Optical Benefit (Covered on Reimbursement basis) Includes: Consultations, Contact Lenses & Optical Lenses only.""")
    Alternative_Medicines: str = Field(..., description="Alternative Medicines")
    Maternity_OP_Benefit: str = Field(..., description="Maternity Operation Benefit")
    Psychiatric_OP_benefit: str = Field(..., description="Psychiatric Operation Benefit")
    Outside_Network_Co_Insurance: str = Field(..., description="Outside Network Co Insurance")
    IP_Benefit: str = Field(..., description="IP Benefit")
    Maternity_IP_benefit: str = Field(..., description="Maternity IP Benefit")
    Psychiatric_IP_benefit: str = Field(..., description="Psychiatric IP Benefit")
    Organ_Transplant: str = Field(..., description="Organ Transplant (including Donor charges but excluding cost of organ)")
    In_patient_cash_benefit_if_Free_of_Charge_treatment_is_taken_free_of_charge_at_a_Govt_Facility_in_UAE: str = Field(..., description="In-patient cash benefit if Free of Charge treatment is taken free of charge at a Govt. Facility in UAE")
    Annual_Health_check_up: str = Field(..., description="Annual Health Check up")
    Value_Added_Services: str = Field(..., description="Value Added Services")
    Gross_Premium_Incl_VAT_and_Basmah: float = Field(..., description="Gross Premium (Incl VAT & Basmah)")
    COST_PER_MEMBER: float = Field(..., description="COST PER MEMBER")


class InsurancesResponse(BaseModel):
    insurances: List[Insurance]

