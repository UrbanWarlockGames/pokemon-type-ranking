import os
import json
import csv
import itertools

def debug(msg):
    print("[DEBUG]", msg)

def load_data(filename):
    """
    Loads the JSON from a file which has:
      'type_ids': { 'Normal':0, 'Fire':1, ... },
      'results': [ {...}, {...} ]
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_single_type_entry(results_list, type_id):
    """
    Given results_list (the array from data['results']) and a single type_id,
    returns the object where entry['types'] == [type_id].
    If not found, returns None.
    """
    for entry in results_list:
        # For a single-type entry, 'entry["types"]' might be [7] for Poison
        if entry.get('types') == [type_id]:
            return entry
    return None

def build_score_map(entry):
    """
    From one single-type entry, build a map: target_type -> score
    using keys: 'c' (coverage), 'or' (offensive resistances),
    'oi' (offensive immunities), 'n' (normal effectiveness).

    For example, if entry["c"] = [{"type":"Grass","score":2.0}], that means
    score_map["Grass"] = 2.0.

    If none of these arrays mention a certain target type, default to 1.0 later.
    """
    debug("    Building score map for a single-type entry")
    score_map = {}

    # Coverage
    coverage_list = entry.get('c', [])
    for matchup in coverage_list:
        tgt = matchup['type']
        val = matchup['score']
        score_map[tgt] = val

    # Offensive Resistances
    off_res_list = entry.get('or', [])
    for matchup in off_res_list:
        tgt = matchup['type']
        val = matchup['score']
        score_map[tgt] = val

    # Offensive Immunities
    off_imm_list = entry.get('oi', [])
    for matchup in off_imm_list:
        tgt = matchup['type']
        val = matchup['score']
        score_map[tgt] = val

    # Normal effectiveness
    normal_list = entry.get('n', [])
    for matchup in normal_list:
        tgt = matchup['type']
        val = matchup['score']
        if tgt not in score_map:
            score_map[tgt] = val

    debug(f"    Single-type score map = {score_map}")
    return score_map

def calculate_offensive_score(requested_type, data):
    """
    Steps:

    0. If requested_type is single, treat it as dual (Poison -> Poison/Poison)
    1. Convert each type name to an ID via data['type_ids']
    2. Find single-type entries in data['results'] for those IDs
    3. Build a score map for each single-type
    4. Gather all possible target types from data['type_ids'].keys()
    5. Compare/merge the two maps
    6. Convert each final multiplier to points
    9. Sum them up
    """
    debug("Step 0: Checking requested type input")
    if '/' in requested_type:
        type_names = requested_type.split('/')
    else:
        type_names = [requested_type, requested_type]
    debug(f"    Dual types determined: {type_names}")

    # data should have 'type_ids' and 'results'
    if 'type_ids' not in data or 'results' not in data:
        raise KeyError("JSON data missing 'type_ids' or 'results' at top level.")

    type_ids_map = data['type_ids']   # e.g. {'Poison':7, 'Water':2, ...}
    results_list = data['results']    # e.g. array of single-type objects

    debug("Step 1: Converting type names to IDs")
    dual_type_ids = []
    for name in type_names:
        if name not in type_ids_map:
            raise KeyError(f"Type '{name}' not found in type_ids. Available: {list(type_ids_map.keys())}")
        tid = type_ids_map[name]
        dual_type_ids.append(tid)
        debug(f"    '{name}' -> {tid}")

    debug("Step 2: Finding single-type entries in results for each ID")
    single_entries = []
    for tid in dual_type_ids:
        entry = find_single_type_entry(results_list, tid)
        if entry is None:
            raise ValueError(f"No single-type data found for type_id={tid} in results.")
        single_entries.append(entry)
        debug(f"    Found entry for type_id={tid} -> (has keys: {list(entry.keys())})")

    debug("Step 3: Building score maps for each single-type entry")
    score_maps = []
    for e in single_entries:
        smap = build_score_map(e)
        score_maps.append(smap)
    debug(f"    Score maps built. Count={len(score_maps)}\n")

    debug("Step 4: Identify all target types from type_ids keys")
    # We'll evaluate this dual type vs. all known type names
    all_target_types = list(type_ids_map.keys())
    debug(f"    Found {len(all_target_types)} possible target types: {all_target_types}\n")

    debug("Step 5: Comparing each chosen type's score for every target type")
    combined_score_map = {}

    def get_score(m, t):
        # If a target type isn't present, default 1.0
        return m.get(t, 1.0)

    map1, map2 = score_maps[0], score_maps[1]
    for tgt in all_target_types:
        s1 = get_score(map1, tgt)
        s2 = get_score(map2, tgt)
        if s1 > s2:
            chosen = s1
        elif s2 > s1:
            chosen = s2
        else:
            chosen = s1  # same
        combined_score_map[tgt] = chosen
        debug(f"    Target='{tgt}', Score1={s1}, Score2={s2}, Combined={chosen}")

    debug("Step 6: Finished merging.\n")

    debug("Step 7: Verifying combined map size & content")
    debug(f"    combined_score_map size={len(combined_score_map)} => {combined_score_map}\n")

    debug("Step 8: Converting each final multiplier to point total")
    scoring_map = {
        2.0:  2.0,
        1.0:  0.0,
        0.5: -2.0,
        0.0: -3.5
    }

    debug("Step 9: Summing final offensive score")
    total_score = 0.0
    for tgt_type, multiplier in combined_score_map.items():
        points = scoring_map.get(multiplier, 0.0)
        total_score += points
        debug(f"    {tgt_type}: multiplier={multiplier}, points={points}")

    debug(f"Final Offensive Score for {requested_type}: {total_score}\n")
    return total_score

def export_combinations_to_csv(combinations, filename, fieldnames):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for combo in combinations:
            row = {
                'First Type': combo[0][0],
                'Second Type': combo[0][1] if len(combo[0]) > 1 else '',
                'Third Type': combo[0][2] if len(combo[0]) > 2 else '',
                'Defensive Score': 0,
                'Offensive Score': combo[1],
                'Total Score': 0
            }
            writer.writerow({key: value for key, value in row.items() if key in fieldnames})

def handle_csv_export(data):
    try:
        type_ids = list(data['type_ids'].keys())
        monotype_combinations = [(types, calculate_offensive_score('/'.join(types), data)) for types in itertools.combinations(type_ids, 1)]
        dualtype_combinations = [(types, calculate_offensive_score('/'.join(types), data)) for types in itertools.combinations(type_ids, 2)]
        tripletype_combinations = [(types, calculate_offensive_score('/'.join(types), data)) for types in itertools.combinations(type_ids, 3)]
        output_dir = os.path.dirname(os.path.abspath(__file__))
        export_combinations_to_csv(monotype_combinations, os.path.join(output_dir, 'monotype_combinations.csv'), ['First Type', 'Defensive Score', 'Offensive Score', 'Total Score'])
        print("Monotype combinations successfully exported to monotype_combinations.csv")
        export_combinations_to_csv(dualtype_combinations, os.path.join(output_dir, 'dualtype_combinations.csv'), ['First Type', 'Second Type', 'Defensive Score', 'Offensive Score', 'Total Score'])
        print("Dual type combinations successfully exported to dualtype_combinations.csv")
        export_combinations_to_csv(tripletype_combinations, os.path.join(output_dir, 'tripletype_combinations.csv'), ['First Type', 'Second Type', 'Third Type', 'Defensive Score', 'Offensive Score', 'Total Score'])
        print("Triple type combinations successfully exported to tripletype_combinations.csv")
    except Exception as e:
        print(f"An error occurred during CSV export: {e}")

def interactive_prompt(data):
    while True:
        print("Enter a type combination (e.g., 'Poison/Water'), 'export_csv' to export, or 'quit' to exit:")
        user_input = input("Type combination: ").strip()
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'export_csv':
            handle_csv_export(data)
        else:
            try:
                score = calculate_offensive_score(user_input, data)
                print(f"Offensive Score for {user_input}: {score}")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pkm_score_path = os.path.join(script_dir, "pkm-scoreGENV.json")
    data = load_data(pkm_score_path)
    interactive_prompt(data)
