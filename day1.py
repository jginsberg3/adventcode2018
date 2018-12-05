from itertools import cycle

# read in data
with open('data/day1_data.txt', 'r') as f:
    numbers = [int(line.strip()) for line in f.readlines()]

# part 1: get final frequency after all changes    
def get_final_frequency(freq_list):
    '''get the final frequency from a list of frequency changes'''
    return sum(freq_list)
    
# part 2: find the first frequency reached twice
def cycle_freqs(freq_list):
    '''cycle through the frequency list, keeping track of the running totals.
    stop once you find a running total you've already seen.'''       
    st = set()
    g = cycle(freq_list)
    running_total = 0
    
    while True:
        num = next(g)
        running_total += num
        
        if running_total in st:
            print(running_total, 'already in set')
            break
            
        else:
            st.add(running_total)
