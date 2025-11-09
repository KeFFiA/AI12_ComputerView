import asyncio
from typing import List, Dict

from Schemas import FieldExtractionResult


async def dump_to_json(data: List[FieldExtractionResult]) -> Dict:
    output: Dict = {}
    for result in data:
        output[result.field] = result.value

    return output

__all__ = [
    "dump_to_json"
]

if __name__ == "__main__":
    data = [
        FieldExtractionResult(confidence=0.95,
                              reason="The context provided mentions an Airbus A321-200PCF with Manufacturer's Serial Number 1487, indicating a single aircraft. There is no mention of multiple aircraft.",
                              field='Aircraft Count', value='1', auto_added_synonyms=[]),
        FieldExtractionResult(confidence=0.95,
                              reason='The context mentions two engine serial numbers (V10953 and V11646), which indicates there are two engines installed on the Airbus A321-200PCF. The A321 is a twin-engine aircraft, so having two engines is standard. Based on this information, the most precise value for the "Engines Count" field is 2.',
                              field='Engines Count', value='2',
                              auto_added_synonyms=['Engine Set Count', 'Engine Configuration Count']),
        FieldExtractionResult(confidence=1.0,
                              reason='The aircraft type is explicitly stated as "Airbus A321-200PCF" in multiple sections of the document.',
                              field='Aircraft Type', value='Airbus A321-200PCF', auto_added_synonyms=[]),
        FieldExtractionResult(confidence=1.0,
                              reason="The value for the field 'MSN' is explicitly stated in the context provided as '1487'. This value is directly mentioned in the document in the context of an Airbus A321-200PCF aircraft.",
                              field='MSN', value='1487', auto_added_synonyms=['Serial ID']),
        FieldExtractionResult(confidence=0.6,
                              reason="The context mentions 'Engine Manufacturer' and 'Manufacturer's catalogue list price', indicating that there is an entity responsible for engine manufacturing. However, the specific name of the engine manufacturer is not provided in the given text. Therefore, while it is clear that there is an 'Engine Manufacturer' involved, the exact identity cannot be determined from the information provided.",
                              field='Engines Manufacture', value='Engine Manufacturer',
                              auto_added_synonyms=[]),
        FieldExtractionResult(confidence=0.8,
                              reason="The context provides the engine type as IAE V2533-A5, which is the most precise value available for the 'Engines Models' field.",
                              field='Engines Models', value='IAE V2533-A5', auto_added_synonyms=[]),
        FieldExtractionResult(confidence=0.9,
                              reason="The context mentions the aircraft's MSN (Manufacture Serial Number) as 1487, but it does not provide the specific serial number for 'Engine1 MSN'. However, it does list two engine serial numbers: V10953 and V11646, which correspond to the two engines. Since these are the only serial numbers provided for the engines, it is reasonable to infer that one of them corresponds to 'Engine1 MSN'. The most precise value available is one of the two numbers, but it is not explicitly stated which is Engine1. Therefore, the field 'Engine1 MSN' cannot be definitively filled with a single, precise value based on the given context.",
                              field='Engine1 MSN', value=None, auto_added_synonyms=[]),
        FieldExtractionResult(confidence=1.0,
                              reason="The value for the field 'Engine2 MSN' is explicitly provided in the context as 'V11646'.",
                              field='Engine2 MSN', value='V11646',
                              auto_added_synonyms=["Engine II Manufacturer's Number",
                                                   "Engine 2 Manufacturer's SN", 'Engine 2 Unique Number']),
        FieldExtractionResult(confidence=0.98,
                              reason="The aircraft registration is explicitly mentioned as 'Malta Registration Mark 9H-CGK' in the context provided.",
                              field='Aircraft Registration', value='9H-CGK',
                              auto_added_synonyms=['Aircraft Reg Details']),
        FieldExtractionResult(confidence=0.0, reason="The field 'Dated' was not found in the provided context.",
                              field='Dated', value=None,
                              auto_added_synonyms=['Date of Event', 'Incident Date', 'Action Date', 'Critical Date',
                                                   'Determination Date', 'Material Date']),
        FieldExtractionResult(confidence=0.98,
                              reason='The term \'Lessee\' is mentioned multiple times in the context, with the most precise value being \'SmartLynx Airlines Malta Ltd\' as explicitly stated in the context: \'lease to SmartLynx Airlines Malta Ltd (" Lessee ").\' This is further corroborated in the note: \'We understand that, pursuant to an aircraft lease agreement dated as of December 20, 2023 (the "Aircraft Lease") between Cross Ocean Aviation (Cargo), as lessor (" Cross Ocean ") and Lessee, you are the owner of and have leased one (1) Airbus model A321-200PCF aircraft... to Lessee.\'',
                              field='Lesse', value='SmartLynx Airlines Malta Ltd', auto_added_synonyms=[]),
        FieldExtractionResult(confidence=0.85,
                              reason="The term 'Lessor' is mentioned multiple times in the document, indicating it is a key party to the lease agreement. However, the specific name or identity of the Lessor is not directly stated in the provided text. The content refers to the Lessor in general contractual terms without disclosing the actual entity or individual name.",
                              field='Lessor', value='Lessor (identity not specified)',
                              auto_added_synonyms=['Lease Lender']),
        FieldExtractionResult(confidence=1.0,
                              reason='The text explicitly states that all payments must be made in Dollars, and specifies that Dollars are the currency of account in all events.',
                              field='Currency', value='Dollars',
                              auto_added_synonyms=['Dollar Amounts', 'Value Measure']),
        FieldExtractionResult(confidence=0.8,
                              reason="The text mentions 'Event of Loss Proceeds' and describes how insurance proceeds are to be applied, but does not provide a specific numerical value for 'Damage Proceeds'. The closest relevant information is the description of how proceeds are to be used, but no exact amount is given.",
                              field='Damage Proceeds', value='Not specified',
                              auto_added_synonyms=['Damage Claim']),
        FieldExtractionResult(confidence=0.0,
                              reason="The provided context does not contain any information related to a 'Threshold' value.",
                              field='Threshold', value=None, auto_added_synonyms=[]),
        FieldExtractionResult(confidence=0.7,
                              reason="The context provides the 'Engine Agreed Value' as $7,000,000, but the 'Aircraft Agreed Value' is not directly stated. There is a mention of 'Agreed Value' in the insurance section, but it does not provide a specific numerical value for the entire aircraft.",
                              field='Aircraft Agreed Value',
                              value='Not explicitly provided in the context.',
                              auto_added_synonyms=['Contract Value', 'Stipulated Asset Value']),
        FieldExtractionResult(confidence=0.95,
                              reason="The context explicitly mentions 'all-risk ground, flight, taxiing, and ingestion aircraft hull insurance for the Agreed Value', which directly corresponds to the 'Aircraft Hull All Risks' field.",
                              field='Aircraft Hull All Risks',
                              value='all-risk ground, flight, taxiing, and ingestion aircraft hull insurance for the Agreed Value',
                              auto_added_synonyms=['Comprehensive Aircraft Coverage',
                                                   'Aircraft Total Loss Insurance']),
        FieldExtractionResult(confidence=0.65,
                              reason="The context mentions that the liability insurance should be in the amount set forth in Appendix 2B, but the specific value for 'Min Liability Coverages' is not provided directly in the given text. It would be necessary to refer to Appendix 2B to obtain the exact figure.",
                              field='Min Liability Coverages', value='Refer to Appendix 2B',
                              auto_added_synonyms=['Primary Liability Insurance',
                                                   'Fundamental Liability Protection']),
        FieldExtractionResult(confidence=0.9,
                              reason='The text explicitly states that any policies carried in accordance with Section 19.4 shall not contain a deductible that exceeds the amount set forth in Appendix 2B, indicating that the deductible is defined there.',
                              field='All Risks Deductible', value='Appendix 2B',
                              auto_added_synonyms=['Complete Risk Deductible'])
    ]

    asyncio.run(dump_to_json(data))
