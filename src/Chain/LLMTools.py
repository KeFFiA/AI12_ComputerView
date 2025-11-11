import json
import re

from sqlalchemy import text
from langchain.agents import initialize_agent, AgentType
from rapidfuzz import process
from langchain.tools import StructuredTool


from Config import LLM_MODEL, AIRCRAFT_PROMPT, llm_tools as logger
from Database import DatabaseClient

client = DatabaseClient()

LEGAL_SUFFIXES = ["LTD", "OU", "SIA", "INC", "LLC", "BV", "GMBH", "AS"]


async def normalize_airline_name(name: str) -> str:
    pattern = r"\b(" + "|".join(LEGAL_SUFFIXES) + r")\b"
    name = re.sub(pattern, "", name, flags=re.IGNORECASE)
    name = re.sub(r"\band/or\b", " ", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+", " ", name).strip()
    return name


async def split_airline_variants(name: str) -> list[str]:
    parts = re.split(r"\s+and/or\s+", name, flags=re.IGNORECASE)
    return [await normalize_airline_name(p) for p in parts]


async def search_airline(name: str):
    """
    Accepts name of airline as argument.
    """
    variants = await split_airline_variants(name)
    async with client.session("main") as session:
        result = await session.execute(text("SELECT name FROM airlines"))
        airlines = [row[0] for row in result.fetchall()]

    for v in variants:
        for a in airlines:
            if v.upper() in a.upper() or a.upper() in v.upper():
                return a

    best_match, score, _ = process.extractOne(" ".join(variants), airlines)
    return best_match if score > 70 else name


async def search_single_column(table_name, column_name, query):
    """
    Accept table_name, column_name, and query as arguments
    """
    async with client.session("main") as session:
        sql = text(f"""
            SELECT {column_name}
            FROM {table_name}
            WHERE {column_name} ILIKE :q
            LIMIT 5
        """)
        result = await session.execute(sql, {"q": f"%{query}%"})
        return [row[0] for row in result.fetchall()]


async def search_aircraft_and_msn(payload):
    """
    Accepts JSON/dict with optional keys: 'msn', 'registration'.
    Tries exact match by MSN first (if numeric), then exact match by registration (case-insensitive),
    then sanitized-equality by registration (ignoring non-alnum).
    If nothing is found, returns the original input unchanged.
    """

    if isinstance(payload, str):
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return {}
    elif isinstance(payload, dict):
        data = payload
    else:
        return {}

    msn_raw = data.get("msn")
    reg_raw = (data.get("registration") or "").strip()

    async def parse_msn(s) -> int | None:
        if s is None:
            return None
        s = str(s)
        digits = re.sub(r"\D", "", s)
        try:
            return int(digits) if digits else None
        except ValueError:
            return None

    result = None
    async with client.session("main") as session:
        msn_num = await parse_msn(msn_raw)
        if msn_num is not None:
            row = await session.execute(
                text("""
                    SELECT msn, reg_num, aircraft_type
                    FROM registrations
                    WHERE msn = :msn
                    LIMIT 1
                """),
                {"msn": msn_num}
            )
            result = row.fetchone()

        if result is None and reg_raw:
            row = await session.execute(
                text("""
                    SELECT msn, reg_num, aircraft_type
                    FROM registrations
                    WHERE UPPER(reg_num) = UPPER(:reg)
                    LIMIT 1
                """),
                {"reg": reg_raw}
            )
            result = row.fetchone()

        if result is None and reg_raw:
            row = await session.execute(
                text("""
                    SELECT msn, reg_num, aircraft_type
                    FROM registrations
                    WHERE regexp_replace(UPPER(reg_num), '[^A-Z0-9]', '', 'g')
                          = regexp_replace(UPPER(:reg),     '[^A-Z0-9]', '', 'g')
                    LIMIT 1
                """),
                {"reg": reg_raw}
            )
            result = row.fetchone()

    if result is None:
        return data

    return {
        "msn": result[0],
        "registration": result[1],
        "aircraft": result[2]
    }


tools = [
    # StructuredTool.from_function(
    #     name="SearchLocation",
    #     func=lambda q: search_single_column("locations", "name", q),
    #     description=""
    # ),
    StructuredTool.from_function(
        name="SearchAirline",
        coroutine=search_airline,
        description="Find the most suitable Airlines. If nothing is found, returns the original JSON unchanged."
    ),
    StructuredTool.from_function(
        name="SearchAircraft",
        coroutine=search_aircraft_and_msn,
        description="""Find an aircraft by MSN or registration.
        Accepts JSON with optional keys 'registration' and 'msn'.
        Tries exact MSN first (numeric), then exact registration (case-insensitive),
        then sanitized equality (ignoring non-alnum).
        If nothing is found, returns the original JSON unchanged."""
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


async def compare_data(data: str | dict):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            raw = await agent.ainvoke({"input": AIRCRAFT_PROMPT.format(data=data)})
            response = raw.get("output") if isinstance(raw, dict) else raw
            if isinstance(response, dict):
                return response
            elif isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())

        except json.JSONDecodeError as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise
            continue

    return None


if __name__ == "__main__":
    import asyncio
    print(asyncio.run(compare_data(data=
        {
        "report_type": "Full and Final",
        "msn": 5074,
        "aircraft": "Airbus A321 -231",
        "registration": "",
        "insured": "SMARTLYNX AIRLINES SIA and/or SMARTLYNX AIRLINES ESTONIA OU and/or SMARTLYNX AIRLINES MALTA LTD",
        "insurer": "Insurers subscribing to a Policy of Insurance (Policy No: B1752GE2200685000) effected through Howden UK Group Limited",
        "cause": "Ground Power Unit impacted lower forward fuselage during ground handling activities",
        "location": "Sabiha Gökçen International Airport, Turkey",
        "dol": "2023-10-08",
        "indemnity_reserve": 483770.99,
        "indemnity_reserve_currency": "USD",
        "paid_to_date": 483770.99,
        "paid_to_date_currency": "USD",
        "summary": "The Insured hereby forever releases and discharges Insurers and their respective directors, servants, agents, successors and assignees from and against any and all claims, liabilities, demands, actions and costs of whatsoever nature and howsoever and whensoever arising by reason of or in respect of the Incident to the Aircraft and whether under the Policy or otherwise.",
        "contact_name": "",
        "contact_title": "",
        "contact_phone": "",
        "contact_email": ""
    }
    # {
    #     "report_type": "First Advice",
    #     "msn": None,
    #     "aircraft": "Airbus A320-251N",
    #     "registration": "TF-PPF",
    #     "insured": "Fly Play",
    #     "insurer": "Starr Underwriting Agents Limited",
    #     "cause": "No. 2 engine Thrust Reverser damaged during installation",
    #     "location": "Montpellier–Méditerranée Airport, France",
    #     "dol": "2025-03-26",
    #     "indemnity_reserve": None,
    #     "indemnity_reserve_currency": None,
    #     "paid_to_date": 8000.0,
    #     "paid_to_date_currency": "GBP",
    #     "summary": "FlyPlay, Airbus A320-251N, Registration TF-PPF, No. 2 engine Thrust Reverser damaged during installation at Montpellier-Méditerranée Airport, France on 26 March 2025. The aircraft was undergoing scheduled maintenance at the Vallair facility. Following damage being sustained by Vallair to the original installed Thrust Reverser (which is being handled as a separate claim), a replacement Thrust Reverser was procured by FlyPlay and shipped to Vallair for installation. During the installation process undertaken by Vallair employees, which involved the Thrust Reverser being lifted in a sling by crane, it came into contact with the No. 6 strut installed on engine No. 2. Preliminary inspections revealed impact deformation to the inner fixed structure, outside of allowable limitations for continued operation. After undertaking detailed damage mapping, the Thrust Reverser was repaired in accordance with the Structural Repair Manual (SRM) by Vallair. McLarens Paris office was able to undertake a survey at the Vallair facility and discuss the extent of the damage sustained and repairs undertaken.",
    #     "contact_name": "Gary Clift",
    #     "contact_title": "Aviation Claims Manager",
    #     "contact_phone": "+44 (0)788 580 3530",
    #     "contact_email": "gary.clift@mclarens.com"
    # }
    )))
