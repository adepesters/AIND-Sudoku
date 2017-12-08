assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

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

    # Find all instances of naked twins
    
    flag = 1
    
    all_naked_twins_boxes = []
    
    while flag:
    
        # finds current naked twins
        naked_twins_boxes = [[box_1, box_2] for box_1 in values.keys() for box_2 in peers[box_1] \
                      if len(values[box_1]) == 2 and len(values[box_2]) == 2 \
                      and values[box_1] == values[box_2] and box_1 != box_2]
      
        # memorizes all naked twins
        all_naked_twins_boxes = all_naked_twins_boxes + naked_twins_boxes
        
        # Eliminate the naked twins as possibilities for their peers
    
        if naked_twins_boxes:
            for idx in range(len(naked_twins_boxes)-1):
                if len(values[naked_twins_boxes[idx][0]]) == 2 and len(values[naked_twins_boxes[idx][1]]) == 2:
                    
                    # for all peers common to the two boxes of twins
                    for peer in set(peers[naked_twins_boxes[idx][0]]).intersection(peers[naked_twins_boxes[idx][1]]):
                        # don't remove values for peers that share the same twin values
                        if values[peer] != values[naked_twins_boxes[idx][0]]:
                            # eliminate twin values from peers
                            values[peer] = values[peer].replace(values[naked_twins_boxes[idx][0]][0],'')
                            values[peer] = values[peer].replace(values[naked_twins_boxes[idx][0]][1],'')
                                        
            # checks for remaining naked twins
            naked_twins_boxes = [[box_1, box_2] for box_1 in values.keys() for box_2 in peers[box_1] \
                                if len(values[box_1]) == 2 and len(values[box_2]) == 2 \
                                and values[box_1] == values[box_2] and box_1 != box_2]
            
            # if new twins appeared during the elimination, repeat. Else, abort
            for twins in naked_twins_boxes:
                if twins not in all_naked_twins_boxes:              
                    flag = 1
                else:
                    flag = 0 
            
        else: 
            flag = 0               
            
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
    
rows = 'ABCDEFGHI'
cols = '123456789'
    
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# indices of diagonal units
diagonal1_idx = [[row + col for row in rows for col in cols if rows.index(row) == cols.index(col)]]
diagonal2_idx = [[row + col for row in rows for col in cols if rows.index(row) + cols.index(col) == 8]]
# adds diagonals units
unitlist = row_units + column_units + square_units + diagonal1_idx + diagonal2_idx
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) # add diagonal constrain

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
        
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

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
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values) # added naked_twins method
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
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
    
    values = grid_values(grid)
          
    return search(values)

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
