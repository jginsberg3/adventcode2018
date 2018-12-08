
# read in data
with open('data/day3_data.txt' ,'r') as f:
    claims = [line.strip() for line in f.readlines()]

test_claim = '#123 @ 3,2: 5x4'
test_claims_2 = [
'#1 @ 1,3: 4x4',
'#2 @ 3,1: 4x4',
'#3 @ 5,5: 2x2'
]

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
    '''return a list of points that a claim covers on the plot.
    plotting with a 1-index, not 0-index (sorry).'''
    id, start_point, cols_rows = parse_claim(claim)

    # col of start of the plotted point is 1 after start point column
    col_start = start_point[0] + 1
    col_end = col_start + cols_rows[0]
    col_range = range(col_start, col_end)  

    # row of start of the plotted point is 1 after start point row
    row_start = start_point[1] + 1
    row_end = row_start + cols_rows[1]
    row_range = range(row_start, row_end)

    # get all combinations of rows and columns
    return [(c,r) for c in col_range for r in row_range]

def get_overlap(claims):
    '''get plots for all claims. 
    check to see which points have been seen more than once. 
    return the total number of points that where seen more than once.'''
    seen_points = set()
    overlap_points = set()
    
    # get a list where each entry is the list of plot points for a claim
    claim_plots = [plot_claim(claim) for claim in claims]
    
    # for each plot, if seen each point already, add it to overlap_points
    for plot in claim_plots:
        for point in plot:
            if point in seen_points:
                overlap_points.add(point)
                seen_points.add(point)
            else:
                seen_points.add(point)
    
    total_overlap_points = len(overlap_points)
    
    return total_overlap_points
    
    
# part 2: find one claim that doens't overlap with any others
def get_all_plot_points(claims):
    '''return all plot points covered by a list of claims.'''
    all_covered_points = set()
    
    claim_plots = [plot_claim(claim) for claim in claims]
    
    for plot in claim_plots:
        for point in plot:
            all_covered_points.add(point)
            
    return all_covered_points

def check_claim(claim_points, covered_points):
    '''check if a claim's points' overlap with a list of covered_points.'''
    return sum([point in covered_points for point in claim_points])
    
def find_free_claim(claims):
    '''this works but boy does it take a while...
    loop through each claim,
    get all other points covered by the rest of the claims,
    test of there's overlap.'''
    for i,claim in enumerate(claims):
        print(i,claim)
        rest_claims = claims[:]
        rest_claims.remove(claim)
        
        covered_points = get_all_plot_points(rest_claims)
        claim_points = plot_claim(claim)
        
        if check_claim(claim_points, covered_points) == 0:
            return claim
    

            
            