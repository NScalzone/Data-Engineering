import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# United States of America Python Dictionary to translate States,
# Districts & Territories to Two-Letter codes and vice versa.
#
# Canonical URL: https://gist.github.com/rogerallen/1583593
#
# Dedicated to the public domain.  To the extent possible under law,
# Roger Allen has waived all copyright and related or neighboring
# rights to this code.  Data originally from Wikipedia at the url:
# https://en.wikipedia.org/wiki/ISO_3166-2:US
#
# Automatically Generated 2024-10-08 07:45:06 via Jupyter Notebook from
# https://gist.github.com/rogerallen/d75440e8e5ea4762374dfd5c1ddf84e0 

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}
    
# invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

acs_path = 'acs2017_county_data.csv'
confirmed_path = 'covid_confirmed_usafacts.csv'
deaths_path = 'covid_deaths_usafacts.csv'

census_df = pd.read_csv(acs_path)
cases_df = pd.read_csv(confirmed_path)
deaths_df = pd.read_csv(deaths_path)

cases_df = cases_df[['County Name', 'State', '2023-07-23']]
deaths_df = deaths_df[['County Name', 'State', '2023-07-23']]
census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']]

# print(f"cases_df column headers: {list(cases_df)}\ndeaths_df column headers: {list(deaths_df)}\ncensus_df column headers: {list(census_df)}")


cases_df['County Name'] = cases_df['County Name'].str.strip()
deaths_df['County Name'] = deaths_df['County Name'].str.strip()

# print(cases_df[cases_df['County Name'] == 'Washington County'])
# print(deaths_df[deaths_df['County Name'] == 'Washington County'])

# print("\ncases_df has ",len(cases_df[cases_df['County Name'] == 'Washington County']), "occurrences of 'Washington County'")
# print("deaths_df has ",len(deaths_df[deaths_df['County Name'] == 'Washington County']), "occurrences of 'Washington County'")

# df = df.drop(df[df['city'] == 'Chicago'].index)
# print('\ntotal columns before removal in cases_df, deaths_df',len(cases_df), len(deaths_df))
cases_df = cases_df.drop(cases_df[cases_df['County Name'] == 'Statewide Unallocated'].index)
deaths_df = deaths_df.drop(deaths_df[deaths_df['County Name'] == 'Statewide Unallocated'].index)

# print("\ncases_df has ",len(cases_df[cases_df['County Name'] == 'Statewide Unallocated']), "occurrences of 'Unallocated'")
# print("deaths_df has ",len(deaths_df[deaths_df['County Name'] == 'Statewide Unallocated']), "occurrences of 'Unallocated'")

# print('\ntotal columns after removal in cases_df, deaths_df',len(cases_df), len(deaths_df))
            
def get_state_string(abbreviation:str) -> str:
    state_string = (list(us_state_to_abbrev.keys())[list(us_state_to_abbrev.values()).index(abbreviation)])      
    return state_string

state_col = cases_df['State']
new_state_col = state_col.apply(get_state_string)
cases_df['State'] = new_state_col
    
deaths_state_col = deaths_df['State']
new_deaths_state_col = deaths_state_col.apply(get_state_string)
deaths_df['State'] = new_deaths_state_col      

keys = cases_df["County Name"] +', ' + cases_df['State']
cases_df['Key'] = keys

keys = deaths_df["County Name"] +', ' + deaths_df['State']
deaths_df['Key'] = keys

keys = census_df["County"] +', ' + census_df['State']
census_df['Key'] = keys


cases_df =cases_df.set_index('Key')
deaths_df = deaths_df.set_index('Key')
census_df = census_df.set_index('Key')

cases_df = cases_df.rename(columns={'2023-07-23':'Cases'})
deaths_df = deaths_df.rename(columns={'2023-07-23':'Deaths'})

# print(cases_df.columns.values.tolist())
# print(deaths_df.columns.values.tolist())

# join_df = cases_df.merge(deaths_df, left_on='Key', right_on='Key')
join_df = cases_df.join(deaths_df, on='Key', how='left',lsuffix='_left', rsuffix='_right')
join_df = join_df.join(census_df, on='Key', how='left',lsuffix='_left', rsuffix='_right')
join_df = join_df.drop(columns=['County Name_left', 'State_left','County Name_right', 'State_right', ])

join_df['CasesPerCap'] = join_df['Cases']/join_df['TotalPop']
join_df['DeathsPerCap'] = join_df['Deaths']/join_df['TotalPop']
# print(join_df.head(),"\n" ,join_df.columns.values.tolist(), "\ntotal rows", len(join_df) )

to_correlate = join_df[['Cases', 'Deaths', 'TotalPop', 'IncomePerCap', "Poverty", 'Unemployment', 'CasesPerCap', 'DeathsPerCap']]

corr_mat = to_correlate.corr(method='pearson')

# print(corr_mat.head())

sns.heatmap(corr_mat, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

plt.title('Correlation Matrix Heatmap')
plt.show()