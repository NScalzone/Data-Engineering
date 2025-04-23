import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

csv_path = 'employees.csv'

data = pd.read_csv(csv_path)

count = 0
name_violations = 0
for i in data['name']:
    count += 1
    if not i:
        print(f"There is an empty name on line {count}")
        name_violations += 1
    
 
date_format = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
count = 0
birthdate_violations = 0
for i in data['birth_date']:
    count += 1
    if not date_format.match(i):
        print(i)
        print(f"date doesn't match on line {count}")
        birthdate_violations += 1
        

year_violations = 0
for i in data['hire_date']:
    year = i[:4]
    if int(year) < 2015:
        year_violations += 1


salary_violations = 0
for i in data['salary']:
    if int(i) > 100000:
        salary_violations += 1



birth_vs_hire_violations = 0
for index, row in data.iterrows():
    count += 1
    i = row['birth_date']
    j = row['hire_date']
    birth_year = i[:4]
    hire_year = j[:4]
    
    # case where a person was hired before they were born - the latest stage of capitalism
    if int(hire_year) < int(birth_year):
        birth_vs_hire_violations += 1

    if int(hire_year) == int(birth_year):
        birth_month = i[5:7]
        hire_month = j[5:7]
        
        if int(hire_month) < int(birth_month):
            birth_vs_hire_violations += 1
    
        if int(hire_month) == int(birth_month):
            birth_day = i[8:]
            hire_day = j[8:]
            
            if int(hire_day) <= int(birth_day):
                birth_vs_hire_violations += 1 

be_your_own_boss = 0
for index, row in data.iterrows():
    count += 1
    i = row['eid']
    j = row['reports_to']
    
    if int(i) == int(j):
        be_your_own_boss += 1


boss_not_listed = 0
for i in data['reports_to']:
    if i not in data['eid'].values:
        boss_not_listed += 1


cities_vs_employees = {}
for i in data['city']:
    if i not in cities_vs_employees:
        cities_vs_employees[i] = 1
    else:
        cities_vs_employees[i] += 1
   
cities_with_less_than_two = 0 
for j in cities_vs_employees:
    if cities_vs_employees[j] <= 1:
        cities_with_less_than_two += 1
        

employees_per_title = {}
for i in data['title']:
    if i not in employees_per_title:
        employees_per_title[i] = 1
    else:
        employees_per_title[i] += 1

popular_job_titles = 0
for i in employees_per_title:
    if employees_per_title[i] > 1:
        popular_job_titles += 1


salaries = []
for i in data['salary']:
    salaries.append(i//1000)

salary_arr = np.array(salaries)
salary_hist = np.histogram(salary_arr)
# plt.hist(salary_hist)
# plt.legend()
# plt.show()

team_size = {}
for i in data['reports_to']:
    if i not in team_size:
        team_size[i] = 1
    else:
        team_size[i] += 1

team_size_values = []
for i in team_size:
    team_size_values.append(team_size[i])

largest_team = max(team_size_values)
smallest_team = min(team_size_values)

team_arr = np.array(team_size_values)
average_team_size = np.average(team_arr)
median_team_size = np.median(team_arr)

team_size_counts = {}
for i in team_size_values:
    if i not in team_size_counts:
        team_size_counts[i] = 1
    else:
        team_size_counts[i] += 1

mode_team_size = 0
how_many_teams = 0
for i in team_size_counts:
    if team_size_counts[i] > how_many_teams:
        how_many_teams = team_size_counts[i]
        mode_team_size = i
print(team_size_counts)
# team_hist = np.histogram(team_arr)
# plt.hist(team_hist)
# plt.show()

print(f"analysis complete. \nThere were {name_violations} name violations\nThere were {birthdate_violations} birth date violations")
print(f"There were {year_violations} year violations")
print(f"There were {salary_violations} salary violations")
print(f"There were {birth_vs_hire_violations} instances in which someone was hired before they were born")
print(f"{be_your_own_boss} employees report/s to themself, rather than someone else")
print(f"{boss_not_listed} employees report to someone with no listed employee identification number")
print(f"There are {cities_with_less_than_two} cities with less than two employees")
print(f"There are {popular_job_titles} job titles held by more than one employee")
print(f"The largest team has {largest_team} employees, the smallest has {smallest_team}, the average team has {average_team_size}, and the median has {median_team_size}")
print(f"The most common team size is {mode_team_size}, with {how_many_teams} teams of that size")