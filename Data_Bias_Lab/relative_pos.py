import pandas as pd
import scipy
import scipy.stats
import numpy as np

datapath = 'trimet_relpos_2022-12-07.csv'

relpos_df = pd.read_csv(datapath)

# print(relpos_df.head(), relpos_df.shape)

relpos = []
vehicles = []
for index, row in relpos_df.iterrows():
    relpos.append(row["RELPOS"])
    if row["VEHICLE_NUMBER"] not in vehicles:
        vehicles.append(row["VEHICLE_NUMBER"])

std_error = scipy.stats.sem(relpos)
std_dev = scipy.stats.tstd(relpos)
mean_all = np.mean(relpos)
total_size = relpos_df.shape[0]
# print(std_error, mean_all)

def t_test(x1, x2, n1, n2, s):
    # x1 is the mean of all the data
    # x2 is the mean of one vehicle worth of data
    # s is total standard error
    # s is the standard deviation of the sample
    # n1 and n2 are the sizes of the whole data set, and the single vehicle respectively
    # print(f"x1: {x1}\nx2: {x2}\nn1: {n1}\nn2: {n2}\ns: {s}")
    # return((x1 - x2)/np.sqrt(s**2 * ((1/n1)+(1/n2))))
    return((x1 - x2)/(s/np.sqrt(n2)))

t_values = {}
for i in vehicles:
    vehicle_data = relpos_df[relpos_df['VEHICLE_NUMBER']== i]
    temp_relpos = []
    for index, row in vehicle_data.iterrows():
        temp_relpos.append(row["RELPOS"])
    
    n2 = vehicle_data.shape[0]
    s2 = scipy.stats.tstd(temp_relpos)
    x2 = np.mean(temp_relpos)
    t = t_test(mean_all, x2, total_size, n2, s2)
    t_values[i] = t
    
print("\nVehicle Number\t| t_value\n-------------------------------------------")
for i in t_values:
    if t_values[i] < 0.005:
        print(i,"\t\t| ", t_values[i])