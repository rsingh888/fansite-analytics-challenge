
import pandas
import datetime
import sys
import re

if len(sys.argv) != 6:
		print("Please provide the path for input file and four output files. Or execute the run.sh")
		sys.exit(1)
input_file = sys.argv[1]
hosts_file = sys.argv[2]
hours_file = sys.argv[3]
resources_file = sys.argv[4]
blocked_file = sys.argv[5]

raw_data  = []
column_names = ["host", "url", "data_size", "timestamp", "error_code"]
df = pandas.DataFrame(columns = column_names)

blocked_hosts = {} 
blocked_starts = {} 
blocked_results = []

blocked_file = open(blocked_file,'w')
start = datetime.datetime.now()
with open(input_file , encoding='utf-8', errors='ignore') as infile:
    for line in infile:
        row_tuple = ()
        host = line.split()[0]
        try:
            url = re.findall('"([^"]*)"', line)[0].split()[1]
        except Exception as ex:
           url = ""
        try:
            data_size = int(line.split()[-1])
        except Exception as ex:
           data_size = 0
        timestamp = line[line.find("[")+1:line.find("]")]

        error_code = line.split()[-2]
        timestamp_d = datetime.datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')
        row_tuple = (host, url, data_size, timestamp_d, error_code)
        raw_data.append(row_tuple)
        if len(raw_data) %100000 == 0:
            print("Lines read :: ", len(raw_data))

        blocked_start = blocked_starts.get(host, None)
        blocked = False
        if error_code == '401':
            if blocked_start is None: #start counting failures
                blocked_starts[host] = timestamp_d
                blocked_hosts[host] = 1
            else:
                if timestamp_d - blocked_start <= datetime.timedelta(seconds=20): #increae count
                    blocked_hosts[host] += 1
                else:   #reset
                    blocked_starts[host] = timestamp_d
                    blocked_hosts[host] = 1
            if blocked_hosts.get(host, 0) > 3: # now host is blocked for 5 mins
                blocked = True
        else:
            if blocked_start is not None and (timestamp_d - blocked_start) > datetime.timedelta(seconds=300):
                blocked_starts.pop(host)
                blocked_hosts.pop(host)
            if blocked_hosts.get(host, 0) >= 3: # if the failure attempt of a host larger than 3 times, blocked
                blocked = True
        if blocked:
            blocked_file.write(line)

blocked_file.close()
print("blocked file created....")

df = pandas.DataFrame(raw_data, columns=column_names)
 # Get count group by host and sort on descending order. Write to file (hours.txt)
df.groupby([pandas.Grouper(key='host')]).size().reset_index(name='count').sort_values(by='count', ascending=False).head(10).to_csv(hosts_file, index=False, header=False)
print("hosts file created....")

# Sum of data size group by url and sort on descending order. Write to file (hours.txt)
df.groupby(['url'], as_index=False)['data_size'].agg('sum').sort_values(by='data_size', ascending=False).head(10).to_csv(resources_file, index = False, header=False, columns = ['url'])
print("resources file created....")

# Create a dataframe group by timestamp and count and sort on descending order
grouped_df = df.groupby([pandas.Grouper(key='timestamp',freq='H')]).size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
grouped_df['timestamp'] = grouped_df['timestamp'].dt.strftime('%d/%b/%Y:%H:%M:%S %z')
grouped_df.to_csv(hours_file, index=False, header=False)

print("hours file created....")

print("Total time taken in seconds are  :: ", (datetime.datetime.now() - start).total_seconds())
