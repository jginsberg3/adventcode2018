from itertools import combinations

with open('data/day2_data.txt', 'r') as f:
    boxes = [line.strip() for line in f.readlines()]

# get sample for testing    
test_boxes = boxes[:10]


# part 1: getting the checksum
def count_checker(count_list, num):
    '''check if num exists in count_list. use within check_box.'''
    if num in count_list:
        return 1
    else:
        return 0
    
def check_box(box):
    '''parse the box id. return tuple of (2_exits, 3_exists) with 0 or 1 for each digit.'''
    letter_counts = [box.count(letter) for letter in set(box)]
    
    return (count_checker(letter_counts, 2), count_checker(letter_counts,3))
    
def get_checksum(boxes):
    '''check each box then sum up the total 2 and 3 counts. multiply to get checksum.'''
    all_counts = [check_box(box) for box in boxes]
    
    count_2 = sum([box[0] for box in all_counts])
    count_3 = sum([box[1] for box in all_counts])
    checksum = count_2 * count_3
    
    print("Count of 2s: ", count_2)
    print("Count of 3s: ", count_3)
    print("Checksum: ", checksum)



# part 2: find the two boxes with the prototype
def compare_boxes(box1, box2):
    '''compares 2 boxes. return True if boxes are 1 letter off or better, else return False.'''
    comparison = [b1_char == b2_char for b1_char, b2_char in zip(box1, box2)]
    
    if sum(comparison) < len(box1)-1:
        return False
    else:
        return True
    
def get_matching_chars(box1, box2):
    '''for two boxes that almost match, return only the matching characters.'''
    return ''.join([b1_char for b1_char, b2_char in zip(box1, box2) if b1_char == b2_char])
    
def eval_all_boxes(boxes):
    '''loop through all combinations of boxes and compare them. 
    once find the almost-matching boxes, return the matches characters.'''
    for box1, box2 in combinations(boxes, 2):
        if compare_boxes(box1, box2):
            return get_matching_chars(box1, box2)