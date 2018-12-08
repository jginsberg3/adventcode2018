import re
from collections import Counter

with open('data/day4_data.txt', 'r') as f:
    records = [line.strip() for line in f.readlines()]

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


# regex to parse the records
regexp = '\[([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+):([0-9]+)\] (.+)'

def assign_rec_guard(records):
    ''' assigns a guard to a parsed day record.
    use within parse_and_sort() function.'''
    
    day_start_recs = [rec for rec in records if 'Guard' in rec['txt']]
    
    day_guard_dict = {}
    for rec in day_start_recs:
        g = int(re.findall('[0-9]+', rec['txt'])[0])
        #day_guard_dict = {rec['day']: g}
        day_guard_dict.update({rec['day']: g})
        
    for rec in records:
        rec['guard'] = day_guard_dict[rec['day']]
    
    return records
    
    
def add_log_num(records):
    '''assign a log number to keep track of all logs in order.
    use in parse_and_sort() function.'''
    
    for i, rec in enumerate(records):
        rec['lognum'] = i
        
    return records
        
        
def parse_and_sort(records, regexp = regexp):
    '''parse out a list of records and return them sorted in chronological order.'''
    
    parsed_records = [re.match(regexp, record).groups()
                        for record in records]
                        
    #return sorted(parsed_records, key = lambda record: [int(i) for i in record[:-1]])
    
    sorted_records = sorted(parsed_records, key = lambda record: [int(i) for i in record[:-1]])
    
    record_dicts = [{'year': int(rec[0]),
                    'month': int(rec[1]),
                    'day': int(rec[2]),
                    'hour': int(rec[3]),
                    'min': int(rec[4]),
                    'txt': rec[5]}    
                  for rec in sorted_records]
    
    # for guards who start shift before technical start of next day, assign them to next day
    for rec in record_dicts:
        if rec['hour'] > 20:
            rec['day'] += 1

    # assign guard to the day and return results
    #return assign_rec_guard(record_dicts)
    record_dicts = assign_rec_guard(record_dicts)
    record_dicts = add_log_num(record_dicts)
    return record_dicts
    

parsed_records = parse_and_sort(example_records)    
t_p = parsed_records[0]

def get_day_records(records, date):
    '''return records for a single day.'''
    month, day = date
    
    return [rec for rec in records if rec['month'] == month and rec['day'] == day]

def get_day_time_asleep(day_records):
    '''get time asleep.  expects records ONLY FOR A SINGLE DAY.'''
    
    sleep_time = 0
    
    for rec in day_records:
        if rec['txt'] == 'wakes up':
            curr_log_num = rec['lognum']
            prev_rec = [rec for rec in day_records 
                if rec['lognum'] == curr_log_num-1][0]
            
            t_sleep = rec['min'] - prev_rec['min']
            sleep_time += t_sleep
            
    return {'guard': rec['guard'],
        'sleep_time': sleep_time} #'day': rec['day'], 
    


assert get_day_time_asleep(get_day_records(parsed_records, (11,1)))['sleep_time'] == 45
assert get_day_time_asleep(get_day_records(parsed_records, (11,5)))['sleep_time'] == 10
            

def longest_sleeping_guard(records):
    '''get the total mins each guard slept across all days.'''
    
    # get all unique days
    #days = set([rec['day'] for rec in records])
    dates = set([(rec['month'],rec['day']) for rec in records])
    
    # get totals for each day
    day_totals = [get_day_time_asleep(get_day_records(records, date)) for date in dates] 
    
    # get totals across all days for each gaurd
    counts = Counter()
    for day in day_totals:
        counts.update({day['guard']: day['sleep_time']})
    
    return counts
    
    #sleepiest_guard = counts.most_common(1)[0]
    #return {'sleepiest_guard': sleepiest_guard[0], 'mins_asleep': #sleepiest_guard[1]}


sleepiest_guard = longest_sleeping_guard(parsed_records)
#assert sleepiest_guard['sleepiest_guard'] == 10
#assert sleepiest_guard['mins_asleep'] == 50


def min_guard_most_asleep(records, guard):
    '''find the minute numbner a guard was asleep during the most.'''
    
    # get all records for a single guard
    guard_records = [rec for rec in records if rec['guard'] == guard]

    mins_sleeping = Counter()
    
    for rec in guard_records:
        if rec['txt'] == 'wakes up':
            curr_log_num = rec['lognum']
            prev_rec = [rec for rec in guard_records 
                if rec['lognum'] == curr_log_num-1][0]
            
            #t_sleep = rec['min'] - prev_rec['min']
            #sleep_time += t_sleep
            
            sleep_mins = [min for min in range(prev_rec['min'], rec['min'])]
            
            mins_sleeping.update(sleep_mins)
            
    return mins_sleeping.most_common(1)[0][0]   
    
    
#assert min_guard_most_asleep(parsed_records, 10) == 24  


def get_part1_answer(records):
    '''get final answer for part 1.'''
    
    parsed_records = parse_and_sort(records)   
    
    sleepiest_guard = longest_sleeping_guard(parsed_records)
    sleepiest_guard_id = sleepiest_guard['sleepiest_guard'] 
    
    min_most_asleep = min_guard_most_asleep(parsed_records, sleepiest_guard_id)
                        
    answer = {'answer': sleepiest_guard_id * min_most_asleep,
            'sleepiest_guard_id': sleepiest_guard_id,
            'min_most_asleep': min_most_asleep}
    return answer

#assert get_part1_answer(example_records)['answer'] == 240
print(get_part1_answer(example_records))
print(get_part1_answer(records))

p_full_recs = parse_and_sort(records)
sleepy_guard = longest_sleeping_guard(p_full_recs)

