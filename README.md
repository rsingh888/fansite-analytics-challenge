# Fansite-analytics-challenge

This challenge is to perform basic analytics on the server log file, provide useful metrics, and implement basic security measures. 

The desired features are described below: 

### Feature 1: 
List the top 10 most active host/IP addresses that have accessed the site.

### Feature 2: 
Identify the 10 resources that consume the most bandwidth on the site

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods 

### Feature 4: 
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.

## Installation

Python Verison: Python 3.8.2

Required packages:
1. pandas==1.0.3

## Usage
`This application is tested on windows platform using cygwin`

1. Clone the repository
    `git clone https://github.com/rsingh888/fansite-analytics-challenge.git`

2. install required package
    `pip install pandas`

3. Download the actual log file from 
    <https://drive.google.com/file/d/0B7-XWjN4ezogbUh6bUl1cV82Tnc/view>
    place that under  `fansite-analytics-challenge/log_input`

4. Run the program from 
    `cd fansite-analytics-challenge`
    `./run.sh`


## Method

-- Reads the log.txt file and create blocked.txt file as per logic mentioned for feature 4 above.

-- Creates a dataframe with host, url, data_size, timestamp and error/response code (though error code is 
    not needed in the dataframe later, it can be removed to save memory)

-- Create hosts.txt file for feature 1. Logic : Count rows using group by host and sorted by count descending order

-- Create resources.txt file for feature 2. Logic: Sum of data_size using group by url sorted by descending order

-- Creates hours.txt file for feature 3: Logic: Count rows using group by hourly bucket of timestamp and sorted by count descending order

## Output
Output files are created under `log_output` folder
Console output generated as 

```
$ ./run.sh
Lines read ::  100000
Lines read ::  200000
Lines read ::  300000
Lines read ::  400000
Lines read ::  500000
Lines read ::  600000
Lines read ::  700000
Lines read ::  800000
Lines read ::  900000
Lines read ::  1000000
Lines read ::  1100000
Lines read ::  1200000
Lines read ::  1300000
Lines read ::  1400000
Lines read ::  1500000
Lines read ::  1600000
Lines read ::  1700000
Lines read ::  1800000
Lines read ::  1900000
Lines read ::  2000000
Lines read ::  2100000
Lines read ::  2200000
Lines read ::  2300000
Lines read ::  2400000
Lines read ::  2500000
Lines read ::  2600000
Lines read ::  2700000
Lines read ::  2800000
Lines read ::  2900000
Lines read ::  3000000
Lines read ::  3100000
Lines read ::  3200000
Lines read ::  3300000
Lines read ::  3400000
Lines read ::  3500000
Lines read ::  3600000
Lines read ::  3700000
Lines read ::  3800000
Lines read ::  3900000
Lines read ::  4000000
Lines read ::  4100000
Lines read ::  4200000
Lines read ::  4300000
Lines read ::  4400000
blocked file created....
hosts file created....
resources file created....
hours file created....
Total time taken in seconds are  ::  315.731151
```