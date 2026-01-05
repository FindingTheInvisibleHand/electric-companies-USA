import pandas as pd

# Load the dataset
df = pd.read_csv('data/all_generators.csv')

# Function to categorize technology types
def categorize_tech(tech):
    tech = str(tech).lower()
    if any(x in tech for x in ['solar', 'wind', 'hydro', 'biomass', 'landfill gas', 'geothermal']):
        return 'Renewable'
    elif 'nuclear' in tech:
        return 'Nuclear'
    elif any(x in tech for x in ['coal', 'natural gas', 'petroleum', 'oil', 'gas']):
        return 'Fossil'
    elif any(x in tech for x in ['battery', 'storage']):
        return 'Storage'
    else:
        return 'Other'

# Apply the categorization
df['Category'] = df['Technology'].apply(categorize_tech)

# Group by Ticker and Category to sum the capacity
capacity = df.groupby(['Ticker', 'Category'])['Nameplate Capacity (MW)'].sum().unstack(fill_value=0)

# Calculate Total Capacity
capacity['Total Capacity (MW)'] = capacity.sum(axis=1)

# Calculate Percentages
capacity['Renewable %'] = (capacity.get('Renewable', 0) / capacity['Total Capacity (MW)']) * 100
capacity['Fossil %'] = (capacity.get('Fossil', 0) / capacity['Total Capacity (MW)']) * 100
capacity['Nuclear %'] = (capacity.get('Nuclear', 0) / capacity['Total Capacity (MW)']) * 100

# Sort by Renewable % descending
final_df = capacity.sort_values('Renewable %', ascending=False)

# Display the result
print(final_df[['Renewable %', 'Fossil %', 'Nuclear %', 'Total Capacity (MW)']].round(2))

# Optional: Save to CSV
final_df.to_csv('data/company_energy_mix.csv')
