import pandas as pd
import os

from data.subsidiaries import subsidiaries_dict

######################################################
## The data is taken from the EIA's 860 2024 report ##
######################################################

def write_generators_file(path_to_file):
    plants = pd.read_excel(
        "data/2___Plant_Y2024.xlsx",
        skiprows=1,
        usecols=["Plant Code", "Plant Name", "State", "Latitude", "Longitude"],
        engine="openpyxl"
    )

    # The selected columns represent the minimum amount of data needed
    # to uniquely identify a generator
    generators = pd.read_excel(
        "data/3_1_Generator_Y2024.xlsx",
        skiprows=1,
        usecols=["Plant Code", "Utility Name", "Energy Source 1", "Technology",
                 "Generator ID", "Nameplate Capacity (MW)", "Summer Capacity (MW)"],
        engine="openpyxl"
    )

    # Merge them on Plant Code
    merged = pd.merge(generators, plants, on="Plant Code", how="left")
    merged.dropna(inplace=True)

    generators_of_interest = pd.DataFrame()
    for key in subsidiaries_dict.keys():
        company_df = merged[merged['Utility Name'].isin(subsidiaries_dict[key])]
        company_df['Ticker'] = key
        generators_of_interest = pd.concat([generators_of_interest, company_df])

    generators_of_interest.to_csv(path_to_file, index=False)


path_to_file = os.path.join('data', 'all_generators.csv')
write_generators_file(path_to_file)