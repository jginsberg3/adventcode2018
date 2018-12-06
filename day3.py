
# read in data
###### JG NOTE: CHANGE THIS TO READ FROM DATA FOLDER ONCE MOVE IT THERE!!!!!!!!!
with open('data/day3_data.txt' ,'r') as f:
    claims = [line.strip() for line in f.readlines()]


#ex: '#1 @ 935,649: 22x22'

# part 1: find fabric overlap
def parse_claim(claim):
    '''parse out info from a claim.'''
    split_claim = claim.split(' ')

    id = split_claim[0]

    start_point = split_claim[2][:-1]
    start_point = tuple([int(i) for i in start_point.split(',')])

    cols_rows = split_claim[3]
    cols_rows = tuple([int(i) for i in cols_rows.split('x')])

    return id, start_point, cols_rows

def plot_claim(claim):
    '''return a list of points that a claim covers on the plot.'''
    id, start_point, cols_rows = parse_claim(claim)

    # col of start of the plotted point is 1 after start point column
    col_start = start_point[0] + 1
    col_end = col_start + cols_rows[0]
    col_range = range(col_start, col_end + 1)

    # row of start of the plotted point is 1 after start point row
    row_start = start_point[1] + 1
    row_end = row_start + cols_rows[1]
    row_range = range(row_start, row_end + 1)

    # get all combinations of rows and columns
    return [(c,r) for c in col_range for r in row_range]
