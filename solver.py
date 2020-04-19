sudoku = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def print_sudoku(sudoku):
    for i in range(len(sudoku)):
        if i % 3 == 0 and i != 0:
            print("---------------------")
        for j in range(len(sudoku[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            if j == 8:
                print(sudoku[i][j])
            else:
                print(str(sudoku[i][j])+" ", end="")


def same_row(sudoku, row, number):
    for j in range(0,9):
        if(sudoku[row][j] == number):
            return True
    return False


def same_col(sudoku, col, number):
    for i in range(0,9):
        if(sudoku[i][col] == number):
            return True
    return False


def same_box(sudoku, row, col, number):
    for r in range((row//3)*3, ((row//3) + 1)*3):
        for c in range((col//3)*3, ((col//3) + 1)* 3):
            if(sudoku[r][c] == number):
                return True
    return False


def is_valid(sudoku, row, col, number):
    if(not same_row(sudoku, row, number) and not same_col(sudoku, col, number) and not same_box(sudoku, row, col, number)):
        return True
    return False


def solve(sudoku):
    for i in range(0, 9):
        for j in range(0, 9):
            if(sudoku[i][j] == 0):
                for n in range(1, 10):
                    if(is_valid(sudoku, i, j, n)):
                        sudoku[i][j] = n
                        if(solve(sudoku)):
                            return True
                        sudoku[i][j] = 0
                return False
    return True


# print_sudoku(sudoku)

# solve(sudoku)
# print("Solved")
# print_sudoku(sudoku)
