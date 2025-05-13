# Defining the type chart for single types
# Values: 0.5 (Not very effective), 2.0 (Super effective), 1.0 (Neutral), 0.0 (No effect)
import json
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

type_chart = {
    "Normal": {"Rock": 0.5, "Ghost": 0.0, "Grass": 1.0, "Fire": 1.0, "Flying": 1.0, "Bug": 1.0, "Psychic": 1.0, "Normal": 1.0, "Ice": 1.0, "Poison": 1.0, "Ground": 1.0, "Fighting": 1.0, "Electric": 1.0, "Water": 1.0, "Dragon": 1.0},
    "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Flying": 1.0, "Psychic": 1.0, "Normal": 1.0, "Poison": 1.0, "Ground": 1.0, "Fighting": 1.0, "Electric": 1.0, "Ghost": 1.0},
    "Water": {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0, "Dragon": 0.5, "Flying": 1.0, "Bug": 1.0, "Psychic": 1.0, "Normal": 1.0, "Ice": 1.0, "Poison": 1.0, "Fighting": 1.0, "Electric": 1.0, "Ghost": 1.0},
    "Electric": {"Water": 2.0, "Electric": 0.5, "Grass": 0.5, "Ground": 0.0, "Flying": 2.0, "Dragon": 0.5, "Fire": 1.0, "Bug": 1.0, "Psychic": 1.0, "Normal": 1.0, "Ice": 1.0, "Poison": 1.0, "Fighting": 1.0, "Rock": 1.0, "Ghost": 1.0},
    "Grass": {"Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, "Dragon": 0.5, "Psychic": 1.0, "Normal": 1.0, "Ice": 1.0, "Fighting": 1.0, "Electric": 1.0, "Ghost": 1.0},
    "Ice": {"Fire": 1.0, "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Bug": 1.0, "Psychic": 1.0, "Normal": 1.0, "Poison": 1.0, "Fighting": 1.0, "Electric": 1.0, "Rock": 1.0, "Ghost": 1.0},
    "Fighting": {"Fighting": 1.0, "Normal": 2.0, "Ice": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2.0, "Ghost": 0.0, "Grass": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Ground": 1.0, "Dragon": 1.0},
    "Poison": {"Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Ice": 1.0, "Flying": 1.0, "Bug": 2.0, "Psychic": 1.0, "Normal": 1.0, "Fighting": 1.0, "Dragon": 1.0},
    "Ground": {"Ground": 1.0, "Fire": 2.0, "Electric": 2.0, "Grass": 0.5, "Poison": 2.0, "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Water": 1.0, "Psychic": 1.0, "Normal": 1.0, "Ice": 1.0, "Fighting": 1.0, "Ghost": 1.0, "Dragon": 1.0},
    "Flying": {"Flying": 1.0, "Electric": 0.5, "Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, "Rock": 0.5, "Fire": 1.0, "Water": 1.0, "Psychic": 1.0, "Normal": 1.0, "Ice": 1.0, "Poison": 1.0, "Ground": 1.0, "Ghost": 1.0, "Dragon": 1.0},
    "Psychic": {"Ground": 1.0, "Psychic": 1.0, "Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Grass": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Ice": 1.0, "Flying": 1.0, "Bug": 1.0, "Rock": 1.0, "Ghost": 1.0, "Normal": 1.0, "Dragon": 1.0},
    "Bug": {"Bug": 1.0, "Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 2.0, "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Electric": 1.0, "Water": 1.0, "Ground": 1.0, "Rock": 1.0, "Ice": 1.0, "Normal": 1.0, "Dragon": 1.0},
    "Rock": {"Rock": 1.0, "Fire": 2.0, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5, "Flying": 2.0, "Bug": 2.0, "Water": 1.0, "Grass": 1.0, "Electric": 1.0, "Psychic": 1.0, "Normal": 1.0, "Poison": 1.0, "Ghost": 1.0, "Dragon": 1.0},
    "Ghost": {"Fighting": 1.0,"Normal": 0.0, "Psychic": 0.0, "Ghost": 2.0, "Grass": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Ice": 1.0, "Flying": 1.0, "Bug": 1.0, "Rock": 1.0, "Ground": 1.0, "Poison": 1.0, "Dragon": 1.0},
    "Dragon": {"Dragon": 2.0, "Grass": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Ice": 1.0, "Flying": 1.0, "Bug": 1.0, "Psychic": 1.0, "Normal": 1.0, "Poison": 1.0, "Ground": 1.0, "Rock": 1.0, "Ghost": 1.0, "Fighting": 1.0},
}

def get_defensive_strengths_weaknesses(pokemon_type):
    if pokemon_type not in type_chart:
        return "Invalid Pokémon type. Please choose from the available types."

    # Initialize dictionaries to store the results
    weaknesses = {}
    resistances = {}
    immunities = {}
    neutrals = {}
    coverage = {}
    offensive_resistances = {}
    offensive_immunities = {}

    # Iterate through the type chart to determine matchups
    for attack_type, matchups in type_chart.items():
        effectiveness = matchups.get(pokemon_type, 1.0)
        if effectiveness == 2.0:
            if attack_type in weaknesses:
                weaknesses[attack_type] *= 2  # Handle quad weaknesses
            else:
                weaknesses[attack_type] = effectiveness
        elif effectiveness == 0.5:
            if attack_type in resistances:
                resistances[attack_type] *= 0.5  # Handle quad resistances
            else:
                resistances[attack_type] = effectiveness
        elif effectiveness == 0.0:
            immunities[attack_type] = effectiveness
        elif effectiveness == 1.0:
            neutrals[attack_type] = effectiveness

    # Determine coverage (super effective matchups for attack type)
    for defending_type, effectiveness in type_chart[pokemon_type].items():
        if effectiveness >= 2.0:
            if defending_type in coverage:
                coverage[defending_type] += effectiveness
            else:
                coverage[defending_type] = effectiveness
        elif effectiveness == 0.5:
            if defending_type in offensive_resistances:
                offensive_resistances[defending_type] *= 0.5  # Handle multiple resistances
            else:
                offensive_resistances[defending_type] = effectiveness
        elif effectiveness == 0.0:
            offensive_immunities[defending_type] = effectiveness

    return {
        "Weaknesses": weaknesses,
        "Resistances": resistances,
        "Immunities": immunities,
        "Neutrals": neutrals,
        "Coverage": coverage,
        "Offensive_Resistances": offensive_resistances,
        "Offensive_Immunities": offensive_immunities
    }

def get_dual_type_defensive_strengths_weaknesses(pokemon_types):
    type1, type2 = pokemon_types.split('/')
    if type1 not in type_chart or type2 not in type_chart:
        return "Invalid Pokémon types. Please choose from the available types."

    # Initialize dictionaries to store the results
    weaknesses = {}
    resistances = {}
    immunities = {}
    neutrals = {}
    coverage = {}
    offensive_resistances = {}
    offensive_immunities = {}

    # Iterate through the type chart to determine matchups for both types
    for attack_type in type_chart:
        effectiveness_type1 = type_chart[attack_type].get(type1, 1.0)
        effectiveness_type2 = type_chart[attack_type].get(type2, 1.0)

        # Handle immunities and neutral types
        combined_effectiveness = effectiveness_type1 * effectiveness_type2

        if combined_effectiveness == 1.0:
            neutrals[attack_type] = combined_effectiveness
        elif combined_effectiveness > 1.0:
            weaknesses[attack_type] = combined_effectiveness
        elif 0.0 < combined_effectiveness < 1.0:
            resistances[attack_type] = combined_effectiveness
        elif combined_effectiveness == 0.0:
            immunities[attack_type] = combined_effectiveness

    # Prioritize immunities over weaknesses and resistances
    for immunity in immunities.keys():
        weaknesses.pop(immunity, None)
        resistances.pop(immunity, None)

    # Determine coverage (super effective matchups for both types)
    for defending_type in set(type_chart[type1].keys()).union(set(type_chart[type2].keys())):
        effectiveness1 = type_chart[type1].get(defending_type, 1.0)
        effectiveness2 = type_chart[type2].get(defending_type, 1.0)

        combined_effectiveness = effectiveness1 * effectiveness2
        if combined_effectiveness >= 2.0:
            coverage[defending_type] = combined_effectiveness
        elif combined_effectiveness == 0.5:
            offensive_resistances[defending_type] = combined_effectiveness
        elif combined_effectiveness == 0.0:
            offensive_immunities[defending_type] = combined_effectiveness

    return {
        "Weaknesses": weaknesses,
        "Resistances": resistances,
        "Immunities": immunities,
        "Neutrals": neutrals,
        "Coverage": coverage,
        "Offensive_Resistances": offensive_resistances,
        "Offensive_Immunities": offensive_immunities
    }

def get_tri_type_defensive_strengths_weaknesses(pokemon_types):
    type1, type2, type3 = pokemon_types.split('/')
    if type1 not in type_chart or type2 not in type_chart or type3 not in type_chart:
        return "Invalid Pokémon types. Please choose from the available types."

    # Initialize dictionaries to store the results
    weaknesses = {}
    resistances = {}
    immunities = {}
    neutrals = {}
    coverage = {}
    offensive_resistances = {}
    offensive_immunities = {}

    # Iterate through the type chart to determine matchups for all three types
    for attack_type in type_chart:
        effectiveness_type1 = type_chart[attack_type].get(type1, 1.0)
        effectiveness_type2 = type_chart[attack_type].get(type2, 1.0)
        effectiveness_type3 = type_chart[attack_type].get(type3, 1.0)

        combined_effectiveness = effectiveness_type1 * effectiveness_type2 * effectiveness_type3

        if combined_effectiveness == 1.0:
            neutrals[attack_type] = combined_effectiveness
        elif combined_effectiveness > 1.0:
            weaknesses[attack_type] = combined_effectiveness
        elif 0.0 < combined_effectiveness < 1.0:
            resistances[attack_type] = combined_effectiveness
        elif combined_effectiveness == 0.0:
            immunities[attack_type] = combined_effectiveness

    # Prioritize immunities over weaknesses and resistances
    for immunity in immunities.keys():
        weaknesses.pop(immunity, None)
        resistances.pop(immunity, None)

    # Determine coverage (super effective matchups for all three types)
    for defending_type in set(type_chart[type1].keys()).union(set(type_chart[type2].keys())).union(set(type_chart[type3].keys())):
        effectiveness1 = type_chart[type1].get(defending_type, 1.0)
        effectiveness2 = type_chart[type2].get(defending_type, 1.0)
        effectiveness3 = type_chart[type3].get(defending_type, 1.0)

        combined_effectiveness = effectiveness1 * effectiveness2 * effectiveness3
        if combined_effectiveness >= 2.0:
            coverage[defending_type] = combined_effectiveness
        elif combined_effectiveness == 0.5:
            offensive_resistances[defending_type] = combined_effectiveness
        elif combined_effectiveness == 0.0:
            offensive_immunities[defending_type] = combined_effectiveness

    return {
        "Weaknesses": weaknesses,
        "Resistances": resistances,
        "Immunities": immunities,
        "Neutrals": neutrals,
        "Coverage": coverage,
        "Offensive_Resistances": offensive_resistances,
        "Offensive_Immunities": offensive_immunities
    }

def export_results_to_json(filename="type_analysis_resultsGENI.json"):
    results = {}
    # Analyze all single types
    for pokemon_type in type_chart.keys():
        results[pokemon_type] = get_defensive_strengths_weaknesses(pokemon_type)

    # Analyze all dual types
    for type1 in type_chart.keys():
        for type2 in type_chart.keys():
            if type1 != type2:
                dual_type = f"{type1}/{type2}"
                results[dual_type] = get_dual_type_defensive_strengths_weaknesses(dual_type)

    # Analyze all tri types (just for demonstration, could be exhaustive)
    for type1 in type_chart.keys():
        for type2 in type_chart.keys():
            for type3 in type_chart.keys():
                if len({type1, type2, type3}) == 3:  # Ensure all three types are unique
                    tri_type = f"{type1}/{type2}/{type3}"
                    results[tri_type] = get_tri_type_defensive_strengths_weaknesses(tri_type)

    # Write results to JSON file
    with open(filename, "w") as json_file:
        json.dump(results, json_file, indent=4)
    print(f"Results successfully exported to {filename}")

def main():
    print("Welcome to the Pokémon Type Defensive Strength/Weakness Calculator!")
    print("Available Types: Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon")

    # Get user input for Pokémon type, dual types, or tri types
    user_type = input("Enter a Pokémon type, dual types (e.g., Fire or Ghost/Psychic), or tri types (e.g., Fire/Water/Grass) to analyse: ")

    if user_type.count('/') == 1:
        # Retrieve strengths and weaknesses for dual types
        results = get_dual_type_defensive_strengths_weaknesses(user_type)
    elif user_type.count('/') == 2:
        # Retrieve strengths and weaknesses for tri types
        results = get_tri_type_defensive_strengths_weaknesses(user_type)
    else:
        # Retrieve strengths and weaknesses for single type
        results = get_defensive_strengths_weaknesses(user_type)

    # Display results
    if isinstance(results, str):
        print(results)
    else:
        print("\nDefensive analysis for type(s):", user_type.capitalize())
        print("Weaknesses:", ", ".join([f"{k} (x{v})" for k, v in results["Weaknesses"].items()]) or "None")
        print("Resistances:", ", ".join([f"{k} (x{v})" for k, v in results["Resistances"].items()]) or "None")
        print("Immunities:", ", ".join(results["Immunities"].keys()) or "None")
        print("Neutrals:", ", ".join(results["Neutrals"].keys()) or "None")

        # Add a line break between Defensive and Offensive analysis
        print("\nOffensive analysis:")
        print("Coverage (Super Effective Against):", ", ".join([f"{k} (x{v})" for k, v in results["Coverage"].items()]) or "None")
        print("Resistances (Not Very Effective Against):", ", ".join([f"{k} (x{v})" for k, v in results["Offensive_Resistances"].items()]) or "None")
        print("Immunities (No Effect Against):", ", ".join(results["Offensive_Immunities"].keys()) or "None")

    # Export results to JSON file
    export_results_to_json()

if __name__ == "__main__":
    main()