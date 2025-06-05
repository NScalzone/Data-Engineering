from faker import Faker
import pandas as pd
import random
import datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

roles_and_salaries_df = pd.read_csv('Departments Roles and Salaries - RolesAndSalaries.csv')

emp_df = pd.DataFrame(columns=[
    'employeeID',
    'CountryOfBirth', 
    'name', 
    'phone', 
    'email', 
    'gender',
    'birthdate',
    'hiredate',
    'department',
    'role',
    'salary',
    'SSID']
)


locality = {
    "USA":"en_US", 
    "India":"ta_IN", 
    "China":"zh_CN", 
    "Mexico":"es_MX", 
    "Canada":"en_CA", 
    "Philippines":"en_PH", 
    "Taiwan":"zh_TW", 
    "South Korea":"ko"
    }

locality_percentage = {
    "USA":0.6,
    "India":(0.4 * 0.745), 
    "China":(0.4 * 0.118), 
    "Mexico":(0.4 * 0.006), 
    "Canada":(0.4 * .01), 
    "Philippines":(0.4 * 0.006), 
    "Taiwan":(0.4 * 0.006), 
    "South Korea":(0.4 * 0.009)
    }

locality_totals = {
    "USA":6000,
    "India":2980, 
    "China":472, 
    "Mexico":24, 
    "Canada":40, 
    "Philippines":24, 
    "Taiwan":24, 
    "South Korea":36
    }
# locality_totals = {
#     "USA":1,
#     "India":1, 
#     "China":1, 
#     "Mexico":1, 
#     "Canada":1, 
#     "Philippines":1, 
#     "Taiwan":1, 
#     "South Korea":1
#     }


departments = {
    "Engineering":30,
    "Product Management":10,
    "Sales":20,
    "Marketing":10,
    "Customer Support":10,
    "IT":6,
    "Human Resources":5,
    "Finance":2,
    "Legal":2,
    "Administrative":4,
    "Executive Leadership":1
    }


def get_id_number(emp_df):
    employeeID = random.randint(100000000,999999999)
    while employeeID in emp_df["employeeID"]:
        employeeID = random.randint(100000000,999999999)
    return employeeID


def get_random_department(departments):
    """
    Returns a department name based on the provided percentage weights.
    """
    department_names = list(departments.keys())
    weights = list(departments.values())
    return random.choices(department_names, weights=weights, k=1)[0]

def get_random_locality(localitities):
    """
    Returns the locality based on the percentages
    """
    locality_names = list(localitities.keys())
    weights = list(localitities.values())
    return random.choices(locality_names, weights=weights, k=1)[0]
 

def get_random_role(df, department):
    """
    Returns a random role from the given department.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing department and role info.
        department (str): Department name to filter roles.
        
    Returns:
        str: A randomly chosen role from the department.
    """
    roles = df[df['Department'] == department]['Role']
    if roles.empty:
        raise ValueError(f"No roles found for department: {department}")
    return random.choice(roles.tolist())

def parse_salary(salary_str):
    """
    Converts a salary string like "$123,000.00" to a float 123000.00.
    """
    return float(salary_str.replace('$', '').replace(',', ''))

def get_random_salary(df, role):
    """
    Returns a random salary within the bounds for a given role.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing role and salary bounds.
        role (str): Role name to look up salary range.
        
    Returns:
        float: A randomly selected salary between the lower and upper bounds.
    """
    row = df[df['Role'] == role]
    if row.empty:
        raise ValueError(f"Role not found: {role}")
    
    lower_str = row['Lower'].values[0]
    upper_str = row['Upper'].values[0]

    lower = parse_salary(lower_str)
    upper = parse_salary(upper_str)

    return int(random.uniform(lower, upper))

def get_unique_name(country, gender, emp_df, locality_map, max_attempts=1000):
    fake = Faker(locality_map[country])
    existing_names = set(emp_df["name"])

    for _ in range(max_attempts):
        if gender == 'male':
            firstname = fake.first_name_male()
        elif gender == 'female':
            firstname = fake.first_name_female()
        else:
            firstname = fake.first_name_nonbinary()

        lastname = fake.last_name()
        name = f"{firstname} {lastname}"

        if name not in existing_names:
            return firstname, lastname

    raise ValueError("Failed to generate a unique name after max attempts.")

def get_unique_email(firstname, lastname, emp_df, locality_map):
    # print(emp_df.head(10))
    fake = Faker(locality_map[country])
    domain = fake.free_email_domain()
    email = f"{firstname}.{lastname}@{domain}"
    tries = 0
    while email in emp_df["email"]:
        if tries == 0:
            email = f"{lastname}.{firstname}@{domain}"
            tries += 1
        if tries == 1:
            email = f"{firstname}{lastname}@{domain}"
            tries += 1
        if tries == 2:
            email = f"{lastname}{firstname}@{domain}"
            tries += 1
        else:
            domain = fake.free_email_domain()
            email = f"{firstname}.{lastname}@{domain}"
            tries = 0
        
    return email

us_fake = Faker('en_US')

for i in tqdm(range(10000)):
    country= get_random_locality(locality_percentage)
    # i is the locality , i.e. "USA"
    fake = Faker(locality[country])
    
    # for j in tqdm(range(locality_totals[country])):
        
    # j is a number based on the total amount for each locality
    employeeID = get_id_number(emp_df)
    countryOfBirth = country
    gender_dice = random.randint(1,100)
    
    if gender_dice <= 49:
        gender = 'male'
    elif gender_dice <= 98:
        gender = 'female'
    else:
        gender = 'nonbinary'
    
    firstname, lastname = get_unique_name(country, gender, emp_df, locality)    
    name = firstname + " " + lastname
    # domain = fake.free_email_domain()
    email = get_unique_email(firstname, lastname, emp_df, locality)
    ssn = us_fake.ssn()
    phone = us_fake.phone_number()
    birthdate = us_fake.date_between(start_date='-60y', end_date='-20y')
    at_least_twenty = birthdate + relativedelta(years=20)
    founding_date = datetime.date(2010, 1, 1)
    
    # if the employee was eligible for hire at the time of founding
    if at_least_twenty < founding_date:
        hiredate = us_fake.date_between(start_date=founding_date)
    else:
        hiredate = us_fake.date_between(start_date=at_least_twenty)

    department = get_random_department(departments)
    role = get_random_role(roles_and_salaries_df, department)
    salary = get_random_salary(roles_and_salaries_df, role)

    emp_df.loc[-1] = [employeeID, countryOfBirth, name, phone, email, gender, birthdate, hiredate, department, role, salary, ssn]
    emp_df.index = emp_df.index + 1 
    emp_df = emp_df.sort_index()
        

# emp_df = emp_df.sample(frac=1)

print(emp_df.describe(include='all'))
print(emp_df.head(10))
print(sum(emp_df["salary"]))
# emp_df.to_csv("emp_df.csv")