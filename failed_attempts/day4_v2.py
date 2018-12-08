import re
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

with open('data/day4_data.txt', 'r') as f:
    full_records = [line.strip() for line in f.readlines()]

example_records = [
'[1518-11-01 00:00] Guard #10 begins shift',
'[1518-11-01 00:05] falls asleep',
'[1518-11-01 00:25] wakes up',
'[1518-11-01 00:30] falls asleep',
'[1518-11-01 00:55] wakes up',
'[1518-11-01 23:58] Guard #99 begins shift',
'[1518-11-02 00:40] falls asleep',
'[1518-11-02 00:50] wakes up',
'[1518-11-03 00:05] Guard #10 begins shift',
'[1518-11-03 00:24] falls asleep',
'[1518-11-03 00:29] wakes up',
'[1518-11-04 00:02] Guard #99 begins shift',
'[1518-11-04 00:36] falls asleep',
'[1518-11-04 00:46] wakes up',
'[1518-11-05 00:03] Guard #99 begins shift',
'[1518-11-05 00:45] falls asleep',
'[1518-11-05 00:55] wakes up'
]
test_record = example_records[0]


# regex to parse the records
#regexp = '\[([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+):([0-9]+)\] (.+)'
regexp = '.*?\[(.*)\].*'

dt_s = re.findall(regexp, test_record)[0]
txt = test_record.split(']')[-1].strip()
dt = datetime.datetime.strptime(dt_s, '%Y-%m-%d %H:%M')
dt_n = dt + relativedelta(years=300)


def parse_record(record, regexp=regexp):
    dt_s = re.findall(regexp, record)[0]
    dt = datetime.datetime.strptime(dt_s, '%Y-%m-%d %H:%M')
    dt_n = dt + relativedelta(years=300) # have to make date in future - too far in past for pandas
    txt = record.split(']')[-1].strip()
    return [dt_n, txt]
    
def make_df(records):
    p_recs = [parse_record(record) for record in records]
    df = pd.DataFrame(p_recs)
    df.columns = ['dt', 'txt']    
    df.sort_values(by='dt', inplace=True)
    return df

testall = make_df(example_records)
#testall = make_df(full_records)

def get_guard(row):
    if 'Guard' in row:
        return int(re.findall('[0-9]+', row)[0])
    else:
        return None

testall['guard'] = testall['txt'].apply(get_guard)
testall['guard'] = testall['guard'].fillna(method='ffill') # interpolate missing values with forward fill
testall['timediff'] = testall['dt'] - testall['dt'].shift() # get time diff for all records vs. prev one
## find total time asleep for each guard
print(testall[testall['txt'] == 'wakes up'].groupby('guard').sum().sort_values('timediff', ascending=False)) 

#testall['dt'].dt.minute

testall['prev_dt'] = testall['dt'].shift()
testall_f = testall.copy().dropna()

#df['range']=df.apply(lambda x : list(range(x['a'],x['b']+1)),1)
testall_f['minsleep'] = testall_f.apply(lambda x: list(range(int(x['dt'].minute),int(x['prev_dt'].minute))), axis=1)