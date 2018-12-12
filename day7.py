INSTRUCTIONS = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''.split('\n')


'''
[Instruc(input='C', output='A'),
 Instruc(input='C', output='F'),
 Instruc(input='A', output='B'),
 Instruc(input='A', output='D'),
 Instruc(input='B', output='E'),
 Instruc(input='D', output='E'),
 Instruc(input='F', output='E')]
'''

test_instruct = INSTRUCTIONS[0]

import re
from typing import List, NamedTuple
from itertools import chain




class Instruc(NamedTuple):
    input: str
    output: str

class Step(NamedTuple):
    name: str
    input: List[str]
    output: List[str]


rgx = 'Step ([A-Z]) must be finished before step ([A-Z]) can begin.'


def parse_instructions(instructions: List[str]) -> List[Instruc]:
    parsed_instructions = []
    
    for i in instructions:
        _in, _out = re.match(rgx, i).groups()
        new_instruc = Instruc(_in, _out)
        parsed_instructions.append(new_instruc)
        
    return parsed_instructions
    
#parse_instructions(INSTRUCTIONS)    

def get_unique_steps(instructions: List[Instruc]) -> List[str]:
    unique_steps = set()
    
    for i in instructions:
        unique_steps.add(i.input)
        unique_steps.add(i.output)
        
    return sorted(unique_steps)
    
#get_unique_steps(parse_instructions(INSTRUCTIONS))

def get_step_details(instructions: List[str]) -> List[Step]:
    p_instructions = parse_instructions(instructions)
    
    all_steps = get_unique_steps(p_instructions)
    
    p_steps = []
    
    for s in all_steps:
        step = Step(s, [], [])
        for i in p_instructions:
            if i.input == s:
                step.output.append(i.output)
        p_steps.append(step)
        
    for i in p_instructions:
        for s in p_steps:
            if i.output == s.name:
                s.input.append(i.input)
        
    return p_steps

#get_step_details(INSTRUCTIONS)      

def OLD_order_steps(steps: List[Step]) -> str:

    remaining_steps = steps
    ordered_steps = []
    next_step_candidates = []
    
    # find first step
    for i_step, step in enumerate(remaining_steps):
        if step.input == []:
            next_step_candidates.append(step)
            remaining_steps.pop(i_step)
    next_step_candidates = sorted(next_step_candidates, key=lambda x: x.name)
    #print(next_step_candidates)
    for s in next_step_candidates:
        ordered_steps.append(s)
    next_step_candidates = []
    
    # subsequent steps:
    #print(remaining_steps)
    for i_step, step in enumerate(remaining_steps):
        #if step.name in [[o for o in o_step.output] for o_step in ordered_steps]:
        if step.name in list(chain.from_iterable([o_step.output for o_step in ordered_steps])):
            next_step_candidates.append(step)
            remaining_steps.pop(i_step)
    next_step_candidates = sorted(next_step_candidates, key=lambda x: x.name)
    #print(next_step_candidates)
    for s in next_step_candidates:
        ordered_steps.append(s)
    next_step_candidates = []
    ###### this way not working great... says F comes after A because both ready after C
    ###### need to do one letter at a time
        
    
    #print(ordered_steps)
    return ordered_steps
        
        
        
def order_steps(steps: List[Step]) -> str:
    run_len = len(steps)
    remaining_steps = steps
    ordered_steps = []
    next_step_candidates = []
    
    while len(ordered_steps) < run_len:
        # get first step:
        if ordered_steps == []:
            for step in remaining_steps:
                if step.input == []:
                    next_step_candidates.append(step)
            next_step = sorted(next_step_candidates, key=lambda x: x.name)[0]
            ordered_steps.append(next_step)
            next_step_loc = remaining_steps.index(next_step)
            remaining_steps.pop(next_step_loc)
        
        # if already past first step:
        else:
            next_step_candidates = []
            for step in remaining_steps:
                if all([i in list(chain.from_iterable([o_step.name for o_step in ordered_steps])) for i in step.input]):
                    next_step_candidates.append(step)
            next_step = sorted(next_step_candidates, key=lambda x: x.name)[0]
            ordered_steps.append(next_step)
            next_step_loc = remaining_steps.index(next_step)
            remaining_steps.pop(next_step_loc)
                
    
    step_order_string = ''.join([s.name for s in ordered_steps])    
    return step_order_string
        
    
    
    
order_steps(get_step_details(INSTRUCTIONS))
assert order_steps(get_step_details(INSTRUCTIONS)) == 'CABDFE'

with open('data/day7_data.txt', 'r') as f:
    instructions = f.read().split('\n')
    
order_steps(get_step_details(instructions))


#### Part 2

