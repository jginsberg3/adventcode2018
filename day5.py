POL = 'dabAcCaCBAcCcaDA'

'''
'dabAcCaCBAcCcaDA'  The first 'cC' is removed.
'dabAaCBAcCcaDA'   This creates 'Aa', which is removed.
'dabCBAcCcaDA'      Either 'cC' or 'Cc' are removed (the result is the same).
'dabCBAcaDA'        No further actions can be taken.
'''

'dabAcCaCBAcCcaDA'


def react(polymer: str) -> str:
    units = list(polymer)
    idxs = [i for i in range(len(units))]  
    deleted = set()
    
    def next_idx(prev_idx: int) -> int:
        for idx in range(prev_idx + 1, len(units)):
            if idx not in deleted:
                return idx
        return len(units)
    
    did_reduct = True
    while did_reduct:
        did_reduct = False

        lo = next_idx(-1)
        hi = next_idx(lo)

        while hi < len(units):
            unit1 = units[lo]
            unit2 = units[hi]
            if unit1.lower() == unit2.lower() and unit1 != unit2:
                deleted.add(lo)
                deleted.add(hi)
                lo = next_idx(hi)
                hi = next_idx(lo)
                did_reduct = True
            else:
                lo = hi
                hi = next_idx(lo)

    return "".join(unit for i, unit in enumerate(units) if i not in deleted)
            
p = react(POL)        
assert react("Aa") == ""
assert react("abBA") == ""
assert react("abAB") == "abAB"
assert react("aabAAB") == "aabAAB"
assert react("dabAcCaCBAcCcaDA") == "dabCBAcaDA"

with open('data/day5_data.txt') as f:
    polymer = f.read().strip()
#print(len(react(polymer)))

chars = {c.lower() for c in polymer}
best = {}

for c in chars:
    print(c)
    polymer_no_c = polymer.replace(c, "").replace(c.upper(), "")
    best[c] = len(react(polymer_no_c))
print(best)