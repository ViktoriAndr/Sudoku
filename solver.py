import random
import math
import sys


def creating_grid(filename):  # создание сетки
    with open(filename) as f:
        grid = f.read().splitlines()

    for i in range(len(grid)):
        grid[i] = grid[i].split(' ')
        for j in range(len(grid[i])):
            grid[i][j] = int(grid[i][j])
            if grid[i][j] == 0:
                grid[i][j] = '.'

    for r in range(len(grid)):
        if len(grid) != len(grid[r]) or not int(math.sqrt(len(grid))):
            return "Sudoku is given incorrectly"

    return grid


# поиск пустых позиций
def find_empty_position(grid):
    for r in range(len(grid)):
        for w in range(len(grid[r])):
            if grid[r][w] == '.':
                return r, w


# значение в ряду
def get_row(values, pos):
    for i in range(len(values)):
        if i == pos[0]:
            return values[i]


# значение в столбце
def get_col(values, pos):
    r, w = pos
    return [values[i][w] for i in range(len(values[w]))]


# заполняем блоки
def get_block(values, pos):
    r, w = pos
    block = int(math.sqrt(len(values)))
    a = block * (r // block)
    b = block * (w // block)
    return [values[a + r][b + w] for r in range(block) for w in range(block)]


# поиск допустимых значений, проверка(check)
def find_possible_values(grid, pos):
    check_col = get_col(grid, pos)
    check_row = get_row(grid, pos)
    check_block = get_block(grid, pos)
    options = list(range(1, len(grid) + 1))  # варианты
    random.shuffle(options)  # перемешиваем последовательность
    new = []
    for i in range(len(options)):
        if options[i] not in check_block \
                and options[i] not in check_row \
                and options[i] not in check_col:
            new.append(options[i])
    return new


# решение сетки
def solve(grid):
    pos = find_empty_position(grid)
    if not pos:
        return grid
    r, w = pos
    for n in find_possible_values(grid, pos):
        grid[r][w] = n
        if solve(grid):
            s = solve(grid)
            return s
        else:
            grid[r][w] = '.'


# проверка условия: рядом не должно быть одинаковых цифр
def condition(grid):
    good_solve = []
    while solve(grid) not in good_solve:
        solve_grid = solve(grid)
        good_line = []
        for x in range(len(solve_grid) - 1):
            for y in range(len(solve_grid[x]) - 1):
                if solve_grid[x][y] == solve_grid[x + 1][y + 1] \
                        or solve_grid[x][y] == solve_grid[x][y+1] \
                        or solve_grid[x][y] == solve_grid[x+1][y]:
                    solve_grid[x][y] = '.'

        for e in range(len(solve_grid) - 1):
            if '.' not in solve_grid[e]:
                good_line.append(solve_grid[e])
        if len(good_line) == len(solve_grid):
            good_solve.append(good_line)
        break

    if len(good_solve) == 0:
        return "No solutions"
    else:
        return good_solve


# поиск всех решений
def all_solutions(grid):
    solutions = []

    while solve(grid) not in solutions:
        solutions.append(solve(grid))
        break

    if len(solutions) == 0:
        return "No solutions"
    else:
        return solutions


sys.argv = creating_grid('cell_2.txt')
print(condition(sys.argv))
for line in all_solutions(sys.argv)[0]:
    print(line)
