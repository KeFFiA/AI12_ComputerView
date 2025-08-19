def enrich_cause(data):
    engine = data.get("aircraft", {}).get("engine")
    if engine and "cause" in data:
        data["cause"] += f"\nEngine Info: {engine}"
    return data

