import numpy as np
import matplotlib.pyplot as plt
from user_csv import read_csv, write_csv

def merge_data(country_file, population_file, species_file):
    """
    Merges data from three CSV files based on the Country column.

    Parameters:
        country_file (str): Path to the country data CSV.
        population_file (str): Path to the population data CSV.
        species_file (str): Path to the threatened species data CSV.

    Returns:
        dict: A dictionary where keys are country names and values are merged data.
    """
    country_data = read_csv(country_file, include_headers=True)
    population_data = read_csv(population_file, include_headers=True)
    species_data = read_csv(species_file, include_headers=True)

    # Convert to dictionaries for easy lookup
    country_dict = {row[0]: row[1:] for row in country_data[1:]}
    population_dict = {row[0]: row[1:] for row in population_data[1:]}
    species_dict = {row[0]: row[1:] for row in species_data[1:]}

    merged_data = {}
    for country in country_dict:
        if country in population_dict and country in species_dict:
            merged_data[country] = {
                "region": country_dict[country][0],
                "sub_region": country_dict[country][1],
                "area": float(country_dict[country][2]),
                "population": list(map(float, population_dict[country])),
                "species": list(map(int, species_dict[country]))
            }

    return merged_data

def calculate_population_change(data, country):
    """
    Calculates the change in population and average population for a given country.

    Parameters:
        data (dict): Merged data dictionary.
        country (str): Country name.

    Returns:
        dict: Population change, average population, and density.
    """
    population = data[country]["population"]
    area = data[country]["area"]
    change = population[-1] - population[0]
    avg_population = np.mean(population)
    density = population[-1] / area

    return {
        "change": change,
        "avg_population": avg_population,
        "density": density
    }

def calculate_species_statistics(data, sub_region):
    """
    Calculates average and total threatened species per country in a sub-region.

    Parameters:
        data (dict): Merged data dictionary.
        sub_region (str): Sub-region name.

    Returns:
        list: Statistics for each country in the sub-region.
    """
    result = []
    for country, info in data.items():
        if info["sub_region"] == sub_region:
            total_species = sum(info["species"])
            avg_species = np.mean(info["species"])
            species_per_sq_km = total_species / info["area"]
            result.append({
                "country": country,
                "avg_species": avg_species,
                "total_species": total_species,
                "species_per_sq_km": species_per_sq_km
            })
    return result

def display_output(change, avg_population, density, species_stats):
    """
    Displays the formatted output in the terminal.

    Parameters:
        change (float): Population change.
        avg_population (float): Average population.
        density (float): Population density.
        species_stats (list): Threatened species statistics.

    Returns:
        None
    """
    print(f"\nThe change in population from 2000 to 2020 is: {change} people")
    print(f"The average population from 2000 to 2020 is: {avg_population:.0f} people")
    print(f"The current population density is: {density:.2f} people per sq km")

    print("\nThe average number of threatened species in each country of the sub-region:")
    print(f"{'Country':<15}{'Avg Species':<15}{'Total Species':<15}{'Species/Sq Km':<15}")
    for stat in species_stats:
        print(f"{stat['country']:<15}{stat['avg_species']:<15.1f}{stat['total_species']:<15}{stat['species_per_sq_km']:<15.6f}")

def main():
    """
    Main function to execute the program.

    Returns:
        None
    """
    # File paths
    country_file = "Country_Data.csv"
    population_file = "Population_Data.csv"
    species_file = "Threatened_Species.csv"

    # Merge data
    data = merge_data(country_file, population_file, species_file)

    # User interaction
    sub_region = input("Please enter a sub-region: ")
    countries_in_sub_region = [country for country, info in data.items() if info["sub_region"] == sub_region]

    if not countries_in_sub_region:
        print("No countries found for the specified sub-region.")
        return

    print(f"Countries in {sub_region}: {', '.join(countries_in_sub_region)}")
    country = input("Please enter a country within the specified sub-region: ")

    if country not in countries_in_sub_region:
        print("Invalid country selection.")
        return

    # Calculate statistics
    pop_stats = calculate_population_change(data, country)
    species_stats = calculate_species_statistics(data, sub_region)

    # Display results
    display_output(pop_stats["change"], pop_stats["avg_population"], pop_stats["density"], species_stats)

if __name__ == "__main__":
    main()