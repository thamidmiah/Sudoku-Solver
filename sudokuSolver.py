import numpy as np

def sudoku_solver(sudoku):
    
    # Checks if the board is a valid board, if not then returns full board with -1s
    if not is_valid_board(sudoku):
        return np.full_like(sudoku, -1)
    
    
    solved_sudoku = np.copy(sudoku)

    if solve(solved_sudoku):
        return solved_sudoku
    else:
        return np.full_like(sudoku, -1)

def solve(board):
    
    find_empty = empty_position(board)

    if find_empty is None:
        return True
    else:
        row, column = find_empty

    # Get valid numbers for the current position
    valid_numbers = get_valid_numbers(board, (row, column))

    # Sort the valid numbers based on the number of remaining legal values for each choice
    valid_numbers.sort(key=lambda num: count_remaining_values(board, (row, column), num))

    # Try numbers in the order of minimum remaining values
    for number in valid_numbers:
        if is_valid(board, number, (row, column)):
            board[row][column] = number

            if solve(board):
                return True

            board[row][column] = 0  # Backtrack if the current placement doesn't lead to a solution

    return False

# Function which returns numbers available for each cell
def get_valid_numbers(board, position):
    row, col = position
    valid_numbers = [i for i in range(1, 10) if is_valid(board, i, (row, col))]
    return valid_numbers


def count_remaining_values(board, position, number):
    row, col = position
    count = 0

    # Check remaining legal values in the row
    count += sum(1 for j in range(9) if j != col and is_valid(board, number, (row, j)))

    # Check remaining legal values in the column
    count += sum(1 for i in range(9) if i != row and is_valid(board, number, (i, col)))

    # Check remaining legal values in the 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    count += sum(1 for i in range(box_row, box_row + 3) for j in range(box_col, box_col + 3) if (i, j) != (row, col) and is_valid(board, number, (i, j)))

    return count


# Function to check if the board is valid or not and checks if there is any duplicates in the sudoku
def is_valid_board(board):
    for i in range(9):
        row_values = set()
        for j in range(9):
            if board[i][j] != 0:
                if board[i][j] in row_values:
                    return False  # Duplicate number in the same row
                row_values.add(board[i][j])
    return True

def is_valid(board, number, position):
    row, col = position

    # Check if number is valid for row
    if number in board[row, :]:
        return False

    # Check if number is valid for column
    if number in board[:, col]:
        return False

    # Check if number is valid for 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    if number in board[box_row:box_row + 3, box_col:box_col + 3]:
        return False

    return True

def empty_position(board):
    empty_cells = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]
    
    # Sort empty cells based on the number of valid options
    empty_cells.sort(key=lambda pos: len(get_valid_numbers(board, pos)))
    
    if empty_cells:
        return empty_cells[0]
    else:
        return None










"""""
import numpy as np

def sudoku_solver(sudoku):
    solved_sudoku = np.copy(sudoku)

    if solve(solved_sudoku):
        return solved_sudoku
    else:
        return np.full_like(sudoku, -1)

def solve(board):
    while True:
        hidden_singles_result = hidden_singles_rows(board) or hidden_singles_columns(board) or hidden_singles_boxes(board)
        if hidden_singles_result:
            position, number = hidden_singles_result
            board[position[0]][position[1]] = number
        else:
            break  # If no hidden singles, proceed with backtracking approach

   
    find = empty_position(board)

    if find is None:
        return True
    else:
        row, column = find

    # Get valid numbers for the current position
    valid_numbers = get_valid_numbers(board, (row, column))

    # Sort the valid numbers based on the number of remaining legal values for each choice
    valid_numbers.sort(key=lambda num: count_remaining_values(board, (row, column), num))

    # Try numbers in the order of minimum remaining values
    for number in valid_numbers:
        if is_valid(board, number, (row, column)):
            board[row][column] = number

            if solve(board):
                return True

            board[row][column] = 0  # Backtrack if the current placement doesn't lead to a solution

    return False

def get_valid_numbers(board, position):
    row, col = position
    valid_numbers = [i for i in range(1, 10) if is_valid(board, i, (row, col))]
    return valid_numbers

def count_remaining_values(board, position, number):
    row, col = position
    count = 0

    # Check remaining legal values in the row
    count += sum(1 for j in range(9) if j != col and is_valid(board, number, (row, j)))

    # Check remaining legal values in the column
    count += sum(1 for i in range(9) if i != row and is_valid(board, number, (i, col)))

    # Check remaining legal values in the 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    count += sum(1 for i in range(box_row, box_row + 3) for j in range(box_col, box_col + 3) if (i, j) != (row, col) and is_valid(board, number, (i, j)))

    return count

def is_valid(board, number, position):
    row, col = position

    # Check if number is valid for row
    if number in board[row, :]:
        return False

    # Check if number is valid for column
    if number in board[:, col]:
        return False

    # Check if number is valid for 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    if number in board[box_row:box_row + 3, box_col:box_col + 3]:
        return False

    return True

def empty_position(board):
    empty_cells = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]
    
    # Sort empty cells based on the number of valid options
    empty_cells.sort(key=lambda pos: len(get_valid_numbers(board, pos)))
    
    if empty_cells:
        return empty_cells[0]
    else:
        return None



def hidden_singles_row(board, row):
    numbers_to_place = set(range(1, 10)) - set(board[row, :])
    for num in numbers_to_place:
        possible_positions = [(row, col) for col in range(9) if board[row, col] == 0 and num in get_valid_numbers(board, (row, col))]
        if len(possible_positions) == 1:
            return possible_positions[0], num
    return None

def hidden_singles_rows(board):
    for row in range(9):
        result = hidden_singles_row(board, row)
        if result:
            return result
    return None

def hidden_singles_column(board, col):
    numbers_to_place = set(range(1, 10)) - set(board[:, col])
    for num in numbers_to_place:
        possible_positions = [(row, col) for row in range(9) if board[row, col] == 0 and num in get_valid_numbers(board, (row, col))]
        if len(possible_positions) == 1:
            return possible_positions[0], num
    return None

def hidden_singles_columns(board):
    for col in range(9):
        result = hidden_singles_column(board, col)
        if result:
            return result
    return None

def hidden_singles_box(board, box_start_row, box_start_col):
    numbers_to_place = set(range(1, 10)) - set(board[box_start_row:box_start_row + 3, box_start_col:box_start_col + 3].flatten())
    for num in numbers_to_place:
        possible_positions = [
            (box_start_row + i, box_start_col + j)
            for i in range(3)
            for j in range(3)
            if board[box_start_row + i, box_start_col + j] == 0 and num in get_valid_numbers(board, (box_start_row + i, box_start_col + j))
        ]
        if len(possible_positions) == 1:
            return possible_positions[0], num
    return None

def hidden_singles_boxes(board):
    for box_start_row in range(0, 9, 3):
        for box_start_col in range(0, 9, 3):
            result = hidden_singles_box(board, box_start_row, box_start_col)
            if result:
                return result
    return None

"""