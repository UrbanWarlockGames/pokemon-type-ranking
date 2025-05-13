import json
import importlib.util
import os

# Import pkmtypes.py if it exists in the same directory
spec = importlib.util.spec_from_file_location("pkmtypes", os.path.join(os.path.dirname(__file__), "pkmtypes.py"))
if spec and spec.loader:
    pkmtypes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pkmtypes)
    type_chart = pkmtypes.type_chart
    get_defensive_strengths_weaknesses = pkmtypes.get_defensive_strengths_weaknesses
    get_dual_type_defensive_strengths_weaknesses = pkmtypes.get_dual_type_defensive_strengths_weaknesses
    get_tri_type_defensive_strengths_weaknesses = pkmtypes.get_tri_type_defensive_strengths_weaknesses
else:
    raise FileNotFoundError("pkmtypes.py not found in the same directory. Please make sure the file is present.")

type_ids = {type_name: idx for idx, type_name in enumerate(type_chart.keys())}

def export_results_to_json(filename="pkm-score.json"):
    results = []
    # Analyze all single types
    for pokemon_type, type_id in type_ids.items():
        analysis = get_defensive_strengths_weaknesses(pokemon_type)
        results.append({"types": [type_id], **flatten_analysis(analysis)})

    # Analyze all dual types
    seen_dual_types = set()
    for type1, id1 in type_ids.items():
        for type2, id2 in type_ids.items():
            if id1 != id2:
                dual_types_sorted = tuple(sorted([id1, id2]))
                if dual_types_sorted not in seen_dual_types:
                    seen_dual_types.add(dual_types_sorted)
                    analysis = get_dual_type_defensive_strengths_weaknesses(f"{type1}/{type2}")
                    results.append({"types": list(dual_types_sorted), **flatten_analysis(analysis)})

    # Analyze all tri types (just for demonstration, could be exhaustive)
    seen_tri_types = set()
    for type1, id1 in type_ids.items():
        for type2, id2 in type_ids.items():
            for type3, id3 in type_ids.items():
                if len({id1, id2, id3}) == 3:
                    tri_types_sorted = tuple(sorted([id1, id2, id3]))
                    if tri_types_sorted not in seen_tri_types:
                        seen_tri_types.add(tri_types_sorted)
                        analysis = get_tri_type_defensive_strengths_weaknesses(f"{type1}/{type2}/{type3}")
                        results.append({"types": list(tri_types_sorted), **flatten_analysis(analysis)})

    # Write results to JSON file
    with open(os.path.join(os.path.dirname(__file__), filename), "w") as json_file:
        json.dump({"type_ids": type_ids, "results": results}, json_file, separators=(',', ':'), indent=None)
    print(f"Results successfully exported to {filename}")

def flatten_analysis(analysis):
    return {
        "w": [{"type": k, "score": v} for k, v in analysis["Weaknesses"].items()],
        "r": [{"type": k, "score": v} for k, v in analysis["Resistances"].items()],
        "i": [{"type": k, "score": v} for k, v in analysis["Immunities"].items()],
        "n": [{"type": k, "score": v} for k, v in analysis["Neutrals"].items()],
        "c": [{"type": k, "score": v} for k, v in analysis["Coverage"].items()],
        "or": [{"type": k, "score": v} for k, v in analysis["Offensive_Resistances"].items()],
        "oi": [{"type": k, "score": v} for k, v in analysis["Offensive_Immunities"].items()]
    }

if __name__ == "__main__":
    export_results_to_json()
