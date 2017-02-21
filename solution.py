assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        #Find obtain all the unique values in the unit
        unique_values = {values[k] for k in unit if len(values[k]) == 2}
        if len(unique_values) > 0:
            d = dict((values[k],0) for k in unit)
            #Get the count of each value within the unit
            for box in unit:
                d[values[box]] += 1
             
            #if count equal 2 for any of the values and the length is two, then remove from the other peers
            for key in d.keys():
                if key in unique_values and d[key] == 2:
                    for box in unit:
                        if key != values[box]:
                            tmp = values[box]
                            tmp = tmp.translate({ord(c): None for c in key})
                            assign_value(values,box,tmp)

                  
    return values
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
   
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag1 = []
diag2 = []
for s,t in zip(rows,cols):
    diag1.append(s+t)
for s,t in zip(rows[::-1],cols):
    diag2.append(s+t)
diag_units = [diag1,diag2]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    layout = cross(rows,cols)
    all_digits = '123456789'
    d = {}
    for i,entry in enumerate(grid):
        if entry == '.':
            d[layout[i]] = all_digits
        else:
            d[layout[i]] = entry
    return d
 

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
 

def eliminate(values):
    for key in values.keys():
        value = values[key]
        if len(value) == 1:
            # We have a box with a single entry.  Check it's peers to see if that value is present in it's string
            for p in peers[key]:
                peer_value = values[p]
                if peer_value.find(value) != -1:
                    pos = peer_value.find(value)
                    #Condition for if the single entry value is at the end of the string
                    if pos == len(peer_value) - 1:
                        assign_value(values,p,peer_value[:pos])
                    else:
                        assign_value(values,p,peer_value[:pos] + peer_value[pos+1:])
    
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            #Creates a list of box locations where the digit is present in the unit
            dplaces = [box for box in unit if digit in values[box]]
            #If the digit is only present in one of the boxes in the  unit then assign that digit to 
            #digit to that box location
            if len(dplaces) == 1:
                assign_value(values,dplaces[0],digit)
    return values
 

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        #Use the Eliminate Strategy
        values = eliminate(values)

        #Use the Only Choice Strategy
        values = only_choice(values)
        
        #Use the Naked Twins Strategy
        values = naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values



def search(values):
    #"Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    
    if len(solved_values) == len(values.keys()):
            return values
    # Choose one of the unfilled squares with the fewest possibilities
    unfilled = [box for box in values.keys() if len(values[box]) > 1]
    l = sorted(unfilled, key = lambda k: len(values[k]))
    unfilled_square = l[0]
    unfilled_values = values[l[0]]
    
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    
    for num in unfilled_values:
        tmp = values.copy()
        tmp[unfilled_square] = num
        attempt = search(tmp)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid_rep = grid_values(grid)
    attempt = search(grid_rep)
    
    if attempt:
        return attempt
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
