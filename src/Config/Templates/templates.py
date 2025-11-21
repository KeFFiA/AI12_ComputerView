from datetime import date

from pydantic import BaseModel, Field


INSURANCE_SURVEYOR_REPORT_CONSTANTS = [
    "Report type", "MSN", "Aircraft type", "Aircraft Registration", "Insured", "Insurer", "Cause of loss",
    "Location of loss", "Date of loss", "Indemnity reserve", "Indemnity reserve currency", "Paid to date",
    "Paid to date currency", "Summary", "Contact name", "Contact title", "Contact phone", "Contact email"
]


LEASE_AGREEMENT_CONSTANTS = {
    "Aircraft Count": "Number of aircrafts, use None if not provided",
    "Engines Count": "Number of engines, use None if not provided",
    "Aircraft Type": "Type of Aircraft, e.g.: Airbus A320. It's necessarily!!",
    "MSN": "Manufacturer Serial Number. Other field names: MSN, Manufacturer Serial Number, Serial Number, Aircraft Serial Number, etc. It's necessarily!!",
    "Engines Manufacture": "Engines manufacture's name. May be locate in 'Engines' block or same.",
    "Engines Models": "Engines models. May be locate in 'Engines' block or same, if not defined - use None, if it is mentioned that the field refers to another file, you must specify the file name.",
    "Engine1 MSN": "Engine No.1 MSN. Other field names: Engine Serial Number, Engine Serial No, Engine Manufacture Serial Number. "
                   "May be locate in 'Engines' block or same, if not defined - use None, if it is mentioned that the field refers to another file, you must specify the file name.",
    "Engine2 MSN": "Engine No.2 MSN. Other field names: Engine Serial Number, Engine Serial No, Engine Manufacture Serial Number. "
                   "May be locate in 'Engines' block or same, if not defined - use None, if it is mentioned that the field refers to another file, you must specify the file name.",
    "Aircraft Registration": "Aircraft registration number. E.g.: YL-LTD. If not defined - use None, if it is mentioned that the field refers to another file, you must specify the file name.",
    "Dated": "The date the agreement was signed",
    "Lessee": "Lessee is described at the beginning of the file, E.g.: Smartlynx Airlines. If not defined - use None",
    "Lessor": "Lessor is described at the beginning of the file, E.g.: BANK OF UTAH. If not defined - use None",
    "Currency": "E.g.: Dollar. If not defined - use Dollar by default",
    "Damage Proceeds Threshold": "Value in Dollar or another Currency. Other field names: Estimated Excess Cost, Notice of Damage, Damage Proceeds Threshold, Damage Notification Threshold, "
                                 "if not defined - use None, if it is mentioned that the field refers to another file, you must specify the file name.",
    "Aircraft Agreed Value": "Value in Dollar or another Currency. Other field names: Casualty Value, Insured Value, Aircraft Agreed Value, Agreed Value, "
                             "if not defined - use None, if it is mentioned that the field refers to another file, you must specify the file name.",
    "Aircraft Hull All Risks": "Value in Dollar or another Currency. Other field names: Liability Insurance Coverage Amount, Aircraft Hull All Risks"
                               "if not defined - use None, if it is mentioned that the field refers to another file, you must specify the file name.",
    "Min Liability Coverages": "Value in Dollar or another Currency. Other field names: Minimum Liability Coverages, Aircraft Third Party, Third Party"
                               "if not defined - use None, if it is mentioned that the field refers to another file, you must specify the file name.",
    "All Risks Deductible": "Value in Dollar or another Currency. Other field names: Deductibles, Deductible, Aircraft Hull Deductible Amount, Aircraft Hull All Risks, Self Insurance Amount, Maximum Deductible Amount, Hull All Risks of Loss or Damage"
                               "if not defined - use None, if it is mentioned that the field refers to another file, you must specify the file name.",
}

__all__ = [
    "LEASE_AGREEMENT_CONSTANTS", "INSURANCE_SURVEYOR_REPORT_CONSTANTS"
]
