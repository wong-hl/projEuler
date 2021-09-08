import os
from copy import deepcopy

import numpy as np

from anytree import AnyNode, RenderTree


def find_trivial_solutions(solutions, which_subset):

    num_solns = 0

    for i in range(9):
        if which_subset == "square":
            row_index = (i // 3) * 3
            col_index = (i % 3) * 3

            subset = solutions[
                row_index : row_index + 3, col_index : col_index + 3
            ].flatten()
        elif which_subset == "row":
            subset = solutions[i, :]
        elif which_subset == "column":
            subset = solutions[:, i]

        for index, _ in enumerate(subset):

            candidate = subset[index]

            if len(candidate) == 1:
                continue

            this_subset = np.delete(subset, index)

            vals_in_other_sets = [x & candidate for x in this_subset]
            if vals_in_other_sets:
                in_other_sets = set.union(*vals_in_other_sets)
                unique = candidate - set(in_other_sets)

                if unique:
                    subset[index] = unique
                    num_solns += 1

        if which_subset == "square":
            solutions[
                row_index : row_index + 3, col_index : col_index + 3
            ] = np.asarray(subset).reshape(3, 3)
        elif which_subset == "row":
            solutions[i, :] = np.asarray(subset)
        elif which_subset == "column":
            solutions[:, i] = np.asarray(subset)

    solutions = update_candidate_solutions(solutions)

    return solutions, num_solns


def update_candidate_solutions(solutions):
    for i in range(9):
        for j in range(9):

            cell_val = solutions[i, j]

            if len(cell_val) != 1:

                fixed_solutions = get_associated_vals(solutions, i, j)

                if cell_val & fixed_solutions:
                    difference = cell_val - fixed_solutions
                    if difference:
                        solutions[i, j] = difference
                    else:
                        raise Exception("Invalid solution present")

    return solutions


def update_subset_preemptive(mask, candidate_set_subset, preemptive_set):
    return np.asarray(
        [
            val - (val & preemptive_set) if len(val) != 1 and not in_set else val
            for val, in_set in zip(candidate_set_subset, mask)
        ]
    )


def solve_preemptive_sets(solutions):
    num_sets_found = 0
    for i in range(9):
        for j in range(9):
            col_sec = (j // 3) * 3
            row_sec = (i // 3) * 3

            cell_val = solutions[i, j]
            cell_len = len(cell_val)

            if cell_len == 1:
                continue

            row_mask = solutions[i, :] <= cell_val

            if row_mask.sum() == cell_len:
                solutions[i, :] = update_subset_preemptive(
                    row_mask, solutions[i, :], cell_val
                )
                solutions = update_candidate_solutions(solutions)
                num_sets_found += 1

            col_mask = solutions[:, j] <= cell_val

            if col_mask.sum() == cell_len:
                solutions[:, j] = update_subset_preemptive(
                    col_mask, solutions[:, j], cell_val
                )
                solutions = update_candidate_solutions(solutions)
                num_sets_found += 1

            sector_mask = (
                solutions[row_sec : row_sec + 3, col_sec : col_sec + 3] <= cell_val
            )

            if sector_mask.sum() == cell_len:
                sector = solutions[
                    row_sec : row_sec + 3, col_sec : col_sec + 3
                ].flatten()
                sector_mask = sector_mask.flatten()
                solutions[
                    row_sec : row_sec + 3, col_sec : col_sec + 3
                ] = update_subset_preemptive(sector_mask, sector, cell_val).reshape(
                    (3, 3)
                )
                solutions = update_candidate_solutions(solutions)
                num_sets_found += 1

    solutions = update_candidate_solutions(solutions)

    return solutions, num_sets_found


def is_completely_solved(solutions):
    length_checker = np.vectorize(len)
    what_lengths = length_checker(solutions) == 1
    if what_lengths.sum() == 81:
        return True
    else:
        return False


def is_sufficiently_solved(solutions):
    target_cells = [1 for x in solutions[0, 0:3] if len(x) != 1]
    if target_cells:
        return False
    else:
        return True



def find_candidate_solutions(puzzle, master_set):
    candidate_solutions = np.empty((9, 9), dtype=set)

    for i in range(9):
        row_val = puzzle[i, :]
        row_set = set(row_val)
        for j in range(9):

            cell_val = puzzle[i, j]

            if cell_val != 0:
                candidate_solutions[i, j] = {cell_val}
            else:
                col_sec = (j // 3) * 3
                row_sec = (i // 3) * 3
                candidate_solutions[i, j] = master_set - (
                    row_set
                    | set(puzzle[:, j])
                    | set(
                        puzzle[row_sec : row_sec + 3, col_sec : col_sec + 3].flatten()
                    )
                )

    return candidate_solutions


def check_solution(solution):
    col_sec = 0
    row_sec = 0

    for i in range(9):
        row_val = solution[i, :]

        if i % 3 == 0:
            row_sec = (i // 3) * 3
            sector_val = solution[
                row_sec : row_sec + 3, col_sec : col_sec + 3
            ].flatten()

        for j in range(9):

            cell_val = solution[i, j]

            if j % 3 == 0:
                col_sec = (j // 3) * 3
                sector_val = solution[
                    row_sec : row_sec + 3, col_sec : col_sec + 3
                ].flatten()

            row_set = set.union(*(np.delete(row_val, j)))
            col_set = set.union(*(np.delete(solution[:, j], i)))
            sector_set = set.union(
                *(np.delete(sector_val, (i - row_sec) * 3 + (j - col_sec)))
            )

            fixed_solutions = row_set | col_set | sector_set

            if cell_val & fixed_solutions:
                print(f"i = {i}, j = {j} has val {cell_val}")
                print(f"row set: {row_set}")
                print(f"row val: {row_val}")
                print(f"col set: {col_set}")
                print(f"sector set: {sector_set}")
                print(f"sector val: {sector_val}")
                raise Exception("INVALID SOLUTION")

    return True

def get_associated_vals(solution, x, y):
    row_sec = (x // 3) * 3
    col_sec = (y // 3) * 3

    row_vals = [z for z in np.delete(solution[x, :], y) if len(z) == 1]
    col_vals = [z for z in np.delete(solution[:, y], x) if len(z) == 1]
    sector_vals = [
        z
        for z in np.delete(
            solution[
                row_sec : row_sec + 3, col_sec : col_sec + 3
            ].flatten(),
            (x - row_sec) * 3 + (y - col_sec),
        )
        if len(z) == 1
    ]

    if row_vals:
        row = set.union(*row_vals)
    else:
        row = set()

    if col_vals:
        col = set.union(*col_vals)
    else:
        col = set()

    if sector_vals:
        sector = set.union(*sector_vals)
    else:
        sector = set()

    return row | col | sector

def puzzle_three_digit_num(solution_vals):
    multiplier = [100, 10, 1]
    return sum([val.pop()*mult for val, mult in zip(solution_vals, multiplier)])

def extract_puzzles_from_file(file_path):
    with open(file_path, "r") as f:
        data = f.readlines()

    store_puzzles = dict()
    puzzle_counter = 0
    row_counter = 0

    for line in data:
        if "Grid" in line:
            store_puzzles[puzzle_counter] = np.zeros((9, 9), dtype=int)
            puzzle_counter += 1
            row_counter = 0
        elif "End" in line:
            return store_puzzles
        else:
            store_puzzles.get(puzzle_counter - 1)[row_counter, :] = np.asarray(
                [int(x) for x in list(line.strip())]
            )
            row_counter += 1



input_file = os.path.join(".", "problem_96", "p096_sudoku.txt")

# with open(input_file, "r") as f:
#     data = f.readlines()

# store_puzzles = dict()
# puzzle_counter = 0
# row_counter = 0


# for line in data:
#     if "Grid" in line:
#         store_puzzles[puzzle_counter] = np.zeros((9, 9), dtype=int)
#         puzzle_counter += 1
#         row_counter = 0
#     elif "End" in line:
#         break
#     else:
#         store_puzzles.get(puzzle_counter - 1)[row_counter, :] = np.asarray(
#             [int(x) for x in list(line.strip())]
#         )
#         row_counter += 1

all_puzzles = extract_puzzles_from_file(input_file)

master_set = set(np.arange(1, 10))
total_sum = 0
subset_names = ["square", "row", "column"]

store_puzzles_2 = dict()
store_puzzles_2[6] = all_puzzles.get(6)

for puzzle in all_puzzles.values():
# for puzzle in store_puzzles_2.values():

    candidate_solutions = find_candidate_solutions(puzzle, master_set)

    total_no_soln = 0
    total_iters = 0

    solved = is_completely_solved(candidate_solutions)

    while not solved:
        counter = total_iters % 3
        candidate_solutions, num_sol_found = find_trivial_solutions(
            candidate_solutions, subset_names[counter]
        )
        solved = is_completely_solved(candidate_solutions)

        if num_sol_found == 0:
            total_no_soln += 1
            # print(total_iters)

        if total_no_soln > 2:
            # print("No trivial solution found")
            break

    if not solved:
        candidate_solutions = update_candidate_solutions(candidate_solutions)
        solved = is_completely_solved(candidate_solutions)
        prev_num_sets_found = 1

        while not solved:
            candidate_solutions, num_sets_found = solve_preemptive_sets(
                candidate_solutions
            )

            solved = is_completely_solved(candidate_solutions)

            if prev_num_sets_found == num_sets_found:
                print("Guessing required")
                print(candidate_solutions)
                break

            prev_num_sets_found = num_sets_found


    if not solved:
        guess_depth = 0
        name = str(guess_depth)
        prev_node = AnyNode(guess_val=None, soln=candidate_solutions)
        root = prev_node
        prev_name = name

        i = 0
        j = 0

        while i < 9 and j < 9 and not solved:
            else_reached = False

            cell_val = candidate_solutions[i, j]
            cell_len = len(cell_val)

            if cell_len == 1:
                j += 1
                if j == 9:
                    i += 1
                    j = 0
                continue

            cell_val = list(cell_val)

            curr_solution = deepcopy(candidate_solutions)

            for index, val in enumerate(cell_val):
                guess = deepcopy(curr_solution)

                fixed_vals = get_associated_vals(guess, i, j)

                if fixed_vals & {val}:
                    this_node = AnyNode(
                        parent=prev_node, guess_val=val, is_valid=False, index=(i, j)
                    )
                    continue

                guess[i, j] = {val}

                try:
                    temp = update_candidate_solutions(guess)
                except Exception:
                    this_node = AnyNode(
                        parent=prev_node, guess_val=val, is_valid=False, index=(i, j)
                    )
                    continue
                else:
                    candidate_solutions = temp
                    else_reached = True
                    this_node = AnyNode(
                        parent=prev_node,
                        guess_val=val,
                        is_valid=True,
                        index=(i, j),
                        soln=temp,
                    )
                    solved = is_completely_solved(temp)
                    if solved:
                        candidate_solutions = temp
                        found_valid = True
                        break

            exit_counter = 0

            found_valid = False
            while not found_valid:
                for child in list(prev_node.children):
                    if child.is_valid:
                        guess_depth += 1
                        prev_node = child
                        i = child.index[0]
                        j = child.index[1]
                        candidate_solutions = child.soln
                        found_valid = True
                        break

                if not found_valid:
                    prev_node.is_valid = False
                    prev_node.soln = None
                    prev_node = prev_node.parent
                    guess_depth -= 1

                    if prev_node is None:
                        break

                exit_counter += 1

                solved = is_completely_solved(candidate_solutions)


            if not found_valid:
                print(RenderTree(root))
                print("Invalid solution")
                break


    if solved:
        check_solution(candidate_solutions)
        puzzle_sum = puzzle_three_digit_num(candidate_solutions[0, 0:3])
        print(puzzle_sum)
        total_sum += puzzle_sum

print(f"Total sum: {total_sum}")
