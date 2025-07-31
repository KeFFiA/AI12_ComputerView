def aggregate_normalized(results: list) -> dict:
    agg = {
        "incident_date": None,
        "locations": set(),
        "events": set(),
        "aircraft": {
            "type": None,
            "registration": None,
            "serial_number": None
        },
        "claim": {
            "claimed": 0.0,
            "deductible": 0.0,
            "net_paid": 0.0,
            "currency": "USD"
        },
        "parties": {
            "insured": set(),
            "insurer": set()
        }
    }

    for r in results:
        n = r.get("normalized", {})
        if not n:
            continue

        if not agg["incident_date"] and n.get("incident_date"):
            agg["incident_date"] = n["incident_date"]

        if isinstance(n.get("locations"), list):
            for loc in n.get("locations", []):
                if loc:
                    agg["locations"].add(loc)

        if isinstance(n.get("events"), list):
            for ev in n["events"]:
                if ev:
                    agg["events"].add(ev)

        ac = n.get("aircraft", {})
        for key in ["type", "registration", "serial_number"]:
            if not agg["aircraft"].get(key) and ac.get(key):
                agg["aircraft"][key] = ac[key]

        claim = n.get("claim", {})
        for key in ["claimed", "deductible", "net_paid"]:
            if claim.get(key):
                agg["claim"][key] = max(agg["claim"].get(key, 0), claim[key])
        if claim.get("currency"):
            agg["claim"]["currency"] = claim["currency"]

        parties = n.get("parties", {})
        if insured := parties.get("insured"):
            agg["parties"]["insured"].update(insured)
        if insurer := parties.get("insurer"):
            agg["parties"]["insurer"].update(insurer)

    # Преобразуем set → list (для JSON)
    agg["locations"] = sorted(agg["locations"])
    agg["events"] = sorted(agg["events"])
    agg["parties"]["insured"] = sorted(agg["parties"]["insured"])
    agg["parties"]["insurer"] = sorted(agg["parties"]["insurer"])

    return agg
