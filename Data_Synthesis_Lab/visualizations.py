from faker import Faker
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
from ImbalancedLearningRegression import gn

emp_df = pd.read_csv("emp_df.csv")

country_counts = emp_df['CountryOfBirth'].value_counts()
department_counts = emp_df['department'].value_counts()

# *** country of birth plot ***

# Plot the bar chart
plt.figure(figsize=(10, 6))
country_counts.plot(kind='bar')

# Add labels and title
plt.title('Employee Count by Country of Birth')
plt.xlabel('Country of Birth')
plt.ylabel('Number of Employees')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()


# *** department plot ***

# plot the bar chart
plt.figure(figsize=(10, 6))
department_counts.plot(kind='bar')

# Add labels and title
plt.title('Employee Count by Department')
plt.xlabel('Department')
plt.ylabel('Number of Employees')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()


# *** hiredate plot ***

# Ensure 'hiredate' is a datetime object (if not already)
emp_df['hiredate'] = pd.to_datetime(emp_df['hiredate'])

# Extract day of the week (name)
hiredates = pd.DataFrame()
hiredates["HireDay"] = emp_df['hiredate'].dt.day_name()
print(hiredates.head(10))

# Count hires by day of the week
# To ensure correct order, use a Categorical dtype
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hireday = pd.Categorical(hiredates['HireDay'], categories=days_order, ordered=True)

hire_counts = hiredates['HireDay'].value_counts().sort_index()

# Plot the bar chart
plt.figure(figsize=(10, 6))
hire_counts.plot(kind='bar')

plt.title('Number of Employees Hired by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Hires')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# *** KDE Plot of salaries ***
sns.kdeplot(emp_df["salary"])

# Setting the X and Y Label
plt.title("Salary KDE Plot")
plt.xlabel('Salary')
plt.ylabel('Probability Density')
plt.show()


# *** employees born each year line chart ***

# # Ensure 'birthdate' is in datetime format
emp_df['birthdate'] = pd.to_datetime(emp_df['birthdate'])

# Extract birth year
emp_df['BirthYear'] = emp_df['birthdate'].dt.year

# Count number of employees born each year
birth_counts = emp_df['BirthYear'].value_counts().sort_index()

# Plot the line chart
plt.figure(figsize=(12, 6))
plt.plot(birth_counts.index, birth_counts.values, marker='o', linestyle='-')

plt.title('Number of Employees Born Each Year')
plt.xlabel('Birth Year')
plt.ylabel('Number of Employees')
plt.grid(True)
plt.tight_layout()
plt.show()


# *** All salaries KDE plot ***

salary_df = emp_df[["department", "salary"]]

plt.figure(figsize=(12, 6))
sns.kdeplot(data=salary_df, x='salary', hue='department', fill=True, common_norm=False, alpha=0.4)

plt.title('Salary Distribution by Department')
plt.xlabel('Salary')
plt.ylabel('Density')
plt.grid(True)
plt.tight_layout()
plt.show()


# *** Sample the data ****
# Calculate age
today = pd.Timestamp.today()
emp_df['birthdate'] = pd.to_datetime(emp_df['birthdate'])
emp_df['age'] = (today - emp_df['birthdate']).dt.days // 365

# Assign weights
emp_df['weight'] = emp_df['age'].apply(lambda age: 3 if 40 <= age <= 49 else 1)

# Sample with weights
smpl_df = emp_df.sample(n=500, weights='weight')

print("\n",smpl_df.describe(include='all'))
print("\n",smpl_df.head(10))



# *** perturb the data ***

prtrb_df = gn(data=emp_df, y="salary")

print("\n",prtrb_df.describe(include='all'))
print("\n",prtrb_df.head(10))