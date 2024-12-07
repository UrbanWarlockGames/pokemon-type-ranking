import itertools
import os
import json
import csv

# Load type data from a JSON file
types_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pkm-score.json')
with open(types_data_path, 'r') as file:
    type_data = json.load(file)

type_ids = type_data['type_ids']
results = type_data['results']

# Bonus multipliers for specific types
# The value is subtracted for each occurrence of the non-super effective type, multiplied by its magnitude (types which you cannot hit with super effective moves)
type_multipliers = {
    'Water': 1.00, 'Normal': 0.45, 'Grass': 0.35, 'Psychic': 0.85,
    'Fire': 1.00, 'Bug': 0.35, 'Electric': 0.65, 'Fighting': 0.85,
    'Poison': 0.45, 'Flying': 1.00, 'Dark': 0.90, 'Ground': 1.50,
    'Ghost': 0.95, 'Dragon': 0.85, 'Rock': 1.00, 'Fairy': 1.00,
    'Steel': 0.90, 'Ice': 1.00
}

# Toggle for applying bonus multipliers
apply_bonus = False

exclude_triple_types = False  # Toggle to exclude triple types

# Defensive multipliers for specific weaknesses
# The value is subtracted for each occurrence of the weakness, multiplied by its magnitude
defence_multipliers = {
    'Ground': 1.00, 'Fire': 1.00, 'Rock': 1.00, 'Water': 1.00, 'Ice': 1.00, 'Fairy': 1.00,
    'Flying': 1.00, 'Fighting': 1.00, 'Steel': 1.00, 'Dark': 1.00, 'Ghost': 1.00,
    'Psychic': 1.00, 'Dragon': 1.00, 'Electric': 1.00, 'Bug': 1.00, 'Grass': 1.00,
    'Poison': 1.00, 'Normal': 1.00
}

def apply_multiplier(value, type_key):
    return value * (type_multipliers[type_key] if apply_bonus and type_key in type_multipliers else 1)

def evaluate_type_combination(types_combination):
    combined_result = {
        'Original_Weaknesses': {}, 'Original_Resistances': {},
        'Weaknesses': {}, 'Resistances': {}, 'Immunities': set(),
        'Coverage': {}, 'Offensive_Resistances': {}, 'Offensive_Immunities': set()
    }

    def merge_dict(target_dict, data_list, original_dict=None):
        for entry in data_list:
            type_key = entry['type']
            score = entry['score']
            if original_dict is not None and type_key not in original_dict:
                original_dict[type_key] = score
            if score > 1:
                # Add to existing weakness or resistance properly without exceeding intended values
                if type_key in target_dict:
                    if target_dict[type_key] == 2 and score == 2:
                        target_dict[type_key] = 4
                    elif target_dict[type_key] == 4 and score == 2:
                        target_dict[type_key] = 6
                    else:
                        target_dict[type_key] = min(target_dict[type_key] * score, 6)
                else:
                    target_dict[type_key] = score
            elif score < 1:
                # If there's both a weakness and a resistance, they cancel out or reduce the multiplier
                if type_key in target_dict:
                    target_dict[type_key] *= score
                    if target_dict[type_key] == 1:
                        del target_dict[type_key]
                else:
                    target_dict[type_key] = score

    for t in types_combination:
        type_index = type_ids[t]
        data = results[type_index]
        merge_dict(combined_result['Weaknesses'], data['w'], combined_result['Original_Weaknesses'])
        merge_dict(combined_result['Resistances'], data['r'], combined_result['Original_Resistances'])
        combined_result['Immunities'].update(entry['type'] for entry in data['i'])
        merge_dict(combined_result['Coverage'], data['c'])
        merge_dict(combined_result['Offensive_Resistances'], data['or'])
        combined_result['Offensive_Immunities'].update(entry['type'] for entry in data['oi'])

    return combined_result

def analyse_combinations(score_type, exclude_triple_types):
    combinations = []
    for i in range(1, 4):
        if exclude_triple_types and i == 3:
            continue
        for types_combination in itertools.combinations(type_ids.keys(), i):
            result = evaluate_type_combination(types_combination)
            score = calculate_score(result, score_type)
            combinations.append((types_combination, score))
    combinations.sort(key=lambda x: x[1], reverse=True)
    return combinations

def calculate_score(result, score_type):
    if score_type == 'defence':
        weaknesses_score = sum(
            apply_multiplier(v, k) for k, v in result['Weaknesses'].items()
        ) * -1

        # Apply additional penalty for specific weaknesses
        if apply_bonus:
            for k, v in result['Weaknesses'].items():
                if k in defence_multipliers:
                    weaknesses_score -= defence_multipliers[k] * v

        resistances_score = sum(apply_multiplier(v, k) for k, v in result['Resistances'].items() if v != 1)
        immunities_score = len(result['Immunities']) * 3.5

        score = resistances_score + immunities_score + weaknesses_score

        # Apply penalty or bonus if weaknesses exceed resistances or vice versa
        if len(result['Weaknesses']) > len(result['Resistances']):
            score -= 1.25 * (len(result['Weaknesses']) - len(result['Resistances']))
        elif len(result['Resistances']) > len(result['Weaknesses']):
            score += 1.25 * (len(result['Resistances']) - len(result['Weaknesses']))
    
    elif score_type == 'offense':
        coverage_score = sum(v for k, v in result['Coverage'].items())

        # Updated resistance score calculation: subtract 2 for each resistance type
        resistance_score = sum(-2 for k, v in result['Offensive_Resistances'].items() if v < 1)

        immunity_score = 0
        for immunity in result['Offensive_Immunities']:
                if immunity in result['Coverage']:
                    immunity_score -= 2  # If a type can hit it for neutral, reduce penalty to -2
                elif immunity not in result['Coverage']:
                    immunity_score -= 3.5

        score = coverage_score + resistance_score + immunity_score

    return score

def print_results(title, types_combination, score, result, is_offensive=False):
    score = round(score, 2)
    print(f"{title}")
    print(f"Types: {', '.join(types_combination)} with score: {score}")
    if not is_offensive:
        print("Weaknesses:", ', '.join([f"{k} (x{v})" for k, v in result['Weaknesses'].items()]))
        print("Resistances:", ', '.join([f"{k} (x{v})" for k, v in result['Resistances'].items() if v != 1]))
        print("Immunities:", ', '.join(result['Immunities']))
    else:
        print("Coverage (Super Effective Against):", ', '.join([f"{k} (x{v})" for k, v in result['Coverage'].items()]))
        print("Resisted By:", ', '.join([f"{k} (x{v})" for k, v in result['Offensive_Resistances'].items() if v < 1]))
        print("Immunities:", ', '.join(result['Offensive_Immunities']))

def export_combinations_to_csv(combinations, filename, is_monotype=False, is_dualtype=False):
    """
    Exports the combinations to a CSV file with the specified filename.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        if is_monotype:
            writer.writerow(["First Type", "Defensive Score", "Offensive Score", "Total Score"])
        elif is_dualtype:
            writer.writerow(["First Type", "Second Type", "Defensive Score", "Offensive Score", "Total Score"])
        else:
            writer.writerow(["First Type", "Second Type", "Third Type", "Defensive Score", "Offensive Score", "Total Score"])

        for combo in combinations:
            row = list(combo[0])  # Types in the combination
            if is_monotype:
                row = [row[0]]  # Only include the first type for monotypes
            elif is_dualtype:
                row = row[:2]  # Only include the first two types for dual types
            else:
                while len(row) < 3:
                    row.append("")  # Fill empty slots for triple types

            row.extend([round(combo[1], 2), round(combo[2], 2), round(combo[3], 2)])  # Scores
            writer.writerow(row)

def handle_csv_export():
    """
    Handles the CSV export functionality, generating separate CSVs for monotypes, dual types, and triple types.
    """
    try:
        monotype_combinations = []
        dualtype_combinations = []
        tripletype_combinations = []

        for i in range(1, 4):
            if exclude_triple_types and i == 3:
                continue

            for types_combination in itertools.combinations(type_ids.keys(), i):
                result = evaluate_type_combination(types_combination)
                defence_score = calculate_score(result, 'defence')
                offense_score = calculate_score(result, 'offense')
                total_score = defence_score + offense_score

                if i == 1:
                    monotype_combinations.append((types_combination, defence_score, offense_score, total_score))
                elif i == 2:
                    dualtype_combinations.append((types_combination, defence_score, offense_score, total_score))
                elif i == 3:
                    tripletype_combinations.append((types_combination, defence_score, offense_score, total_score))

        # Sort by total score in descending order
        monotype_combinations.sort(key=lambda x: x[3], reverse=True)
        dualtype_combinations.sort(key=lambda x: x[3], reverse=True)
        tripletype_combinations.sort(key=lambda x: x[3], reverse=True)

        # Export to CSV files
        output_dir = os.path.dirname(os.path.abspath(__file__))
        
        export_combinations_to_csv(monotype_combinations, os.path.join(output_dir, 'monotype_combinations.csv'), is_monotype=True)
        print("Monotype combinations successfully exported to monotype_combinations.csv")

        export_combinations_to_csv(dualtype_combinations, os.path.join(output_dir, 'dualtype_combinations.csv'), is_dualtype=True)
        print("Dual type combinations successfully exported to dualtype_combinations.csv")

        if not exclude_triple_types:
            export_combinations_to_csv(tripletype_combinations, os.path.join(output_dir, 'tripletype_combinations.csv'))
            print("Triple type combinations successfully exported to tripletype_combinations.csv")

    except Exception as e:
        print(f"An error occurred during CSV export: {e}")

def handle_specific_combination(combination_str):
    types_combination = tuple(t.capitalize() for t in combination_str.split('/'))
    result = evaluate_type_combination(types_combination)
    defence_score = sum(result['Weaknesses'].values()) * -1 + sum(v for v in result['Resistances'].values() if v != 1) + len(result['Immunities']) * 6
    offense_score = sum(result['Coverage'].values()) + sum(v * -1 for k, v in result['Offensive_Resistances'].items() if v < 1) + len(result['Offensive_Immunities']) * -6
    print_results("Defensive Stats for Combination:", types_combination, defence_score, result)
    print_results("\nOffensive Stats for Combination:", types_combination, offense_score, result, is_offensive=True)

def handle_best_total():
    total_combinations = []

    # Calculate total combinations by averaging defence and offense scores
    for i in range(1, 4):
        if exclude_triple_types and i == 3:
            continue
        for types_combination in itertools.combinations(type_ids.keys(), i):
            result = evaluate_type_combination(types_combination)
            defence_score = calculate_score(result, 'defence')
            offense_score = calculate_score(result, 'offense')
            average_score = (defence_score + offense_score)
            total_combinations.append((types_combination, average_score))

    # Sort the combinations based on their average score, descending
    total_combinations.sort(key=lambda x: x[1], reverse=True)

    # Retrieve the best type combination
    best_combination, best_score = total_combinations[0]
    best_result = evaluate_type_combination(best_combination)

    # Print the best type combination
    print_results("Best Type Combination for Overall Score:", best_combination, best_score, best_result)

def handle_export():
    try:
        defence_combinations = analyse_combinations('defence', exclude_triple_types)
        offense_combinations = analyse_combinations('offense', exclude_triple_types)
        total_combinations = []

        # Calculate total combinations by averaging defence and offense scores
        for i in range(1, 4):
            if exclude_triple_types and i == 3:
                continue
            for types_combination in itertools.combinations(type_ids.keys(), i):
                result = evaluate_type_combination(types_combination)
                defence_score = calculate_score(result, 'defence')
                offense_score = calculate_score(result, 'offense')
                average_score = (defence_score + offense_score) / 2
                total_combinations.append((types_combination, average_score))

        # Sort each list of combinations based on their score, in descending order
        defence_combinations.sort(key=lambda x: x[1], reverse=True)
        offense_combinations.sort(key=lambda x: x[1], reverse=True)
        total_combinations.sort(key=lambda x: x[1], reverse=True)

        # Write to files
        output_dir = os.path.dirname(os.path.abspath(__file__))
        
        with open(os.path.join(output_dir, 'bestof-def.txt'), 'w') as def_file:
            for combo, score in defence_combinations:
                def_file.write(f"{'/'.join(combo)} with score: {score}\n")
        print("Defensive rankings successfully exported to bestof-def.txt")

        with open(os.path.join(output_dir, 'bestof-off.txt'), 'w') as off_file:
            for combo, score in offense_combinations:
                off_file.write(f"{'/'.join(combo)} with score: {score}\n")
        print("Offensive rankings successfully exported to bestof-off.txt")

        with open(os.path.join(output_dir, 'bestof-total.txt'), 'w') as total_file:
            for combo, score in total_combinations:
                total_file.write(f"{'/'.join(combo)} with score: {score}\n")
        print("Total rankings successfully exported to bestof-total.txt")

    except Exception as e:
        print(f"An error occurred during export: {e}")

def main():
    while True:
        user_input = input("Enter command (best, <type/type/...>, export, best_total, csv_export, or quit): ").strip().lower()
        if user_input == "best":
            handle_best()
        elif user_input == "export":
            handle_export()
        elif user_input == "csv_export":
            handle_csv_export()
        elif user_input == "best_total":
            handle_best_total()
        elif user_input == "quit":
            break
        elif '/' in user_input:
            handle_specific_combination(user_input)
        else:
            print("Invalid command. Please enter 'best', '<type/type/...>', 'export', 'best_total', 'csv_export', or 'quit'.")

if __name__ == "__main__":
    main()
