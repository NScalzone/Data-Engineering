import pandas as pd

csv_path = 'acs2017_census_tract_data.csv'

data = pd.read_csv(csv_path)

updated = data.dropna()

updated.to_csv('acs2017_census_tract_data_cleaned.csv', index=False)