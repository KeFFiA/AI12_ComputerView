import json
import os
import re

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from langchain.agents import initialize_agent, Tool, AgentType

from Config import llm, AIRCRAFT_PROMPT, setup_logger

logger = setup_logger(__name__)

engine = create_engine(os.getenv("DB_URI_MAIN"))
Session = sessionmaker(bind=engine)

def search_single_column(table_name, column_name, query):
    session = Session()
    sql = text(f"""
        SELECT {column_name}
        FROM {table_name}
        WHERE {column_name} ILIKE :q
        LIMIT 5
    """)
    result = session.execute(sql, {"q": f"%{query}%"}).fetchall()
    session.close()
    return [row[0] for row in result]


def search_aircraft_and_msn(query_json):
    if isinstance(query_json, str):
        try:
            query_json = json.loads(query_json)
        except json.JSONDecodeError:
            return {}

    msn_val = query_json.get("msn", "")
    registration_val = query_json.get("registration", "")

    session = Session()

    sql_msn = text("""
        SELECT msn, reg_num, aircraft_type
        FROM registrations
        WHERE msn::text ILIKE :msn
        LIMIT 1
    """)
    result = session.execute(sql_msn, {"msn": f"%{msn_val}%"}).fetchone()

    if not result:
        sql_reg = text("""
            SELECT msn, reg_num, aircraft_type
            FROM registrations
            WHERE reg_num ILIKE :reg_num
            LIMIT 1
        """)
        result = session.execute(sql_reg, {"reg_num": f"%{registration_val}%"}).fetchone()

    session.close()

    if result:
        return {
            "msn": result[0],
            "registration": result[1],
            "aircraft": result[2]
        }
    else:
        return query_json


tools = [
    # Tool(
    #     name="SearchLocation",
    #     func=lambda q: search_single_column("locations", "name", q),
    #     description="Найти наиболее подходящие географические локации по названию"
    # ),
    # Tool(
    #     name="SearchCause",
    #     func=lambda q: search_single_column("causes", "description", q),
    #     description="Найти наиболее подходящие причины инцидента по описанию"
    # ),
    Tool(
        name="SearchAircraft",
        func=search_aircraft_and_msn,
        description="""Find a record in the aircrafts table by the fields registration and msn.
                    Accepts JSON with keys registration and msn, returns registration, aircraft, and msn."""
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def compare_data(data: str|dict):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = agent.invoke({"input": AIRCRAFT_PROMPT.format(data=data)})

            response = response['output']
            # TODO: Compare result
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

    compare_data(data={
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
})

