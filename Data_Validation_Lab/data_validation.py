import pandas as pd

csv_path = 'employees.csv'

data = pd.read_csv(csv_path)

print(data.head())
        
print(len(data))