from bs4 import BeautifulSoup
import pandas as pd
import io
from date_time import filter_act_time
pd.options.mode.chained_assignment = None  # default='warn'

stop_events_html = 'trimet_stopevents_2022-12-07.html'
bus_2911_path = "stop_events/2025/5/14/2911.html"

def html_to_df(html_path):
    filehandle = open(html_path)

    soup = BeautifulSoup(filehandle, features='html.parser')
    type(soup)

    id_strings = soup.find_all('h2')

    trip_ids = []
    for id in id_strings:
        temp = str(id)
        temp = temp.strip('<h2>')
        temp = temp.strip('Stop events for PDX_TRIP ')
        temp = temp.strip('</h2>')
        trip_ids.append(temp)

    tables = soup.find_all('table')
    table_dfs = []
    id_index = 0

    for table in tables:
        temp = str(table)
        df = pd.read_html(io.StringIO(temp))
        df[0]['trip_id'] = trip_ids[id_index]
        id_index += 1
        table_dfs.append(df)

    whole_table = table_dfs[0][0]
    for i in range(1,len(table_dfs)):
        whole_table = pd.concat([whole_table, table_dfs[i][0]], axis=0)
    
    date = get_date(soup.find("h1"))
    
    whole_table['date'] = date
        
    return whole_table

def get_date(h1_string):

    temp = str(h1_string)
    # print(temp)
    temp = temp.strip('<h1>')
    # print(temp)
    temp = temp.strip('Trimet CAD/AVL stop data for ')
    # print(temp)
    temp = temp.strip('<')
    return temp

def get_timestamp(row):
    date_string = row["date"] + "T" + str(row["arrive_time_hms"])
    return pd.Timestamp(date_string)

def create_table(input_table):
    
    table = input_table[["trip_id","date", "vehicle_number", "arrive_time", "location_id", "ons", "offs"]]
    
    table["arrive_time_hms"] = table["arrive_time"].apply(filter_act_time)
    table["tstamp"] = table.apply(get_timestamp, axis=1)
    table = table.drop(columns=['arrive_time','arrive_time_hms', 'date'])
    
    return table



whole_table = html_to_df(stop_events_html)

# whole_table = html_to_df(bus_2911_path)

stops_df = create_table(whole_table)

# unique_vehicles = len(pd.unique(stops_df['vehicle_number']))
# unique_stops = len(pd.unique(stops_df["location_id"]))

# ons_df = stops_df[["ons"]]
# more_than_1 = ons_df[ons_df >= 1.0].count()

# min_date = stops_df['tstamp'].min()

# max_date = stops_df['tstamp'].max()
# # print("Max values\n",stops_df.max(numeric_only=True),"\nMin values\n", stops_df.min(numeric_only=True))
# print(f"\nThere are {unique_vehicles} unique vehicles\nThere are {unique_stops} unique stops")
# print(f"\nMin tstamp: {min_date}\nMax tstamp: {max_date}")

# print(f"There are {more_than_1} entries where ons >= 1")
# print(f"Out of 93912, there are 19858 with more than one, which is {100 * (19858.0/93912.0)}%")

# 6913
# location_6913_data = stops_df[stops_df['location_id']==6913]

print(stops_df.head(), "\n", stops_df.shape)
# vehicle_4062_data = stops_df[stops_df['vehicle_number']== 4062]
# total_ons = sum(vehicle_4062_data['ons'])
# total_offs = sum(vehicle_4062_data["offs"])
# ons_df = vehicle_4062_data[["ons"]]
# at_least_one_on = ons_df[ons_df >= 1.0].count()
# print(vehicle_4062_data, vehicle_4062_data.shape,"\ntotal boardings:", total_ons, "\ntotal departures:", total_offs)
# print("\nstops with at least one passenger boarding:", at_least_one_on)

vehicle_nums = []
for index, row in stops_df.iterrows():
    if row["vehicle_number"] not in vehicle_nums:
        vehicle_nums.append(row["vehicle_number"])

def chisquare_calc(on, off):
    return((off - on)**2 ) / on

# print(vehicle_nums)
percentage = 21.15
sub_5_alpha_vehicles = {}
all_ons = 0
all_offs = 0
# chi_square = 0
for i in vehicle_nums:
    chi_square = 0
    vehicle_data = stops_df[stops_df['vehicle_number']== i]
    num_of_stop_events = vehicle_data.shape[0]
    total_ons = sum(vehicle_data['ons'])
    total_offs = sum(vehicle_data["offs"])
    chi_square = chisquare_calc(total_ons, total_offs)
    ons_df = vehicle_data[["ons"]]
    at_least_one_boarding = ons_df[ons_df >= 1.0].count()
    # percentage_stops_with_boarding = 100 * (float(at_least_one_boarding)/float(num_of_stop_events))
    # percent_diff =  100.0 * (percentage_stops_with_boarding/percentage)
    # alpha = abs(100.0 - percent_diff)
    # if alpha < 5:
    #     sub_5_alpha_vehicles[i] = [percentage_stops_with_boarding, alpha]
    if chi_square <= 0.05:
        print(f"Vehicle number: {i}\t ons: {total_ons}\toffs: {total_offs}\tX^2: {chi_square}")
    all_ons += total_ons
    all_offs += total_offs
   
    
print(f"Total ons: {all_ons}\tTotal offs: {all_offs}")
# print(f"X^2 for all ons/offs is: {chi_square}")
# print(f"There are: {len(sub_5_alpha_vehicles)} vehicles with alpha less than 5")
# for i in sub_5_alpha_vehicles:
#     print(i,", ", sub_5_alpha_vehicles[i])
    