import os
from copy import deepcopy

import numpy as np

from anytree import AnyNode, RenderTree


def find_trivial_solutions(solutions, which_subset):

    num_solns = 0

    for index in range(9):
        if which_subset == "square":
            row_index = (index // 3) * 3
            col_index = (index % 3) * 3

            subset = solutions[
                row_index : row_index + 3, col_index : col_index + 3
            ].flatten()
        elif which_subset == "row":
            subset = solutions[index, :]
        elif which_subset == "column":
            subset = solutions[:, index]

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
            solutions[index, :] = np.asarray(subset)
        elif which_subset == "column":
            solutions[:, index] = np.asarray(subset)

    solutions = update_candidate_solutions(solutions)

    return solutions, num_solns


def update_candidate_solutions(solutions):
    for row_index in range(9):
        for col_index in range(9):

            cell_val = solutions[row_index, col_index]

            if len(cell_val) != 1:

                fixed_solutions = get_associated_vals(solutions, row_index, col_index)

                if cell_val & fixed_solutions:
                    difference = cell_val - fixed_solutions
                    if difference:
                        solutions[row_index, col_index] = difference
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
    for row_index in range(9):
        for column_index in range(9):
            col_sec = (column_index // 3) * 3
            row_sec = (row_index // 3) * 3

            cell_val = solutions[row_index, column_index]
            cell_len = len(cell_val)

            if cell_len == 1:
                continue

            row_mask = solutions[row_index, :] <= cell_val

            if row_mask.sum() == cell_len:
                solutions[row_index, :] = update_subset_preemptive(
                    row_mask, solutions[row_index, :], cell_val
                )
                solutions = update_candidate_solutions(solutions)
                num_sets_found += 1

            col_mask = solutions[:, column_index] <= cell_val

            if col_mask.sum() == cell_len:
                solutions[:, column_index] = update_subset_preemptive(
                    col_mask, solutions[:, column_index], cell_val
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

    for row_index in range(9):
        row_val = puzzle[row_index, :]
        row_set = set(row_val)
        for column_index in range(9):

            cell_val = puzzle[row_index, column_index]

            if cell_val != 0:
                candidate_solutions[row_index, column_index] = {cell_val}
            else:
                col_sec = (column_index // 3) * 3
                row_sec = (row_index // 3) * 3
                candidate_solutions[row_index, column_index] = master_set - (
                    row_set
                    | set(puzzle[:, column_index])
                    | set(
                        puzzle[row_sec : row_sec + 3, col_sec : col_sec + 3].flatten()
                    )
                )

    return candidate_solutions


def check_solution(solution):
    col_sec = 0
    row_sec = 0

    for row_index in range(9):
        row_val = solution[row_index, :]

        if row_index % 3 == 0:
            row_sec = (row_index // 3) * 3
            sector_val = solution[
                row_sec : row_sec + 3, col_sec : col_sec + 3
            ].flatten()

        for column_index in range(9):

            cell_val = solution[row_index, column_index]

            if column_index % 3 == 0:
                col_sec = (column_index // 3) * 3
                sector_val = solution[
                    row_sec : row_sec + 3, col_sec : col_sec + 3
                ].flatten()

            row_set = set.union(*(np.delete(row_val, column_index)))
            col_set = set.union(*(np.delete(solution[:, column_index], row_index)))
            sector_set = set.union(
                *(
                    np.delete(
                        sector_val, (row_index - row_sec) * 3 + (column_index - col_sec)
                    )
                )
            )

            fixed_solutions = row_set | col_set | sector_set

            if cell_val & fixed_solutions:
                print(f"i = {row_index}, j = {column_index} has val {cell_val}")
                print(f"row set: {row_set}")
                print(f"row val: {row_val}")
                print(f"col set: {col_set}")
                print(f"sector set: {sector_set}")
                print(f"sector val: {sector_val}")
                raise Exception("INVALID SOLUTION")

    return True


def get_associated_vals(solution, row_index, column_index):
    row_sec = (row_index // 3) * 3
    col_sec = (column_index // 3) * 3

    row_vals = [
        z for z in np.delete(solution[row_index, :], column_index) if len(z) == 1
    ]
    col_vals = [
        z for z in np.delete(solution[:, column_index], row_index) if len(z) == 1
    ]
    sector_vals = [
        z
        for z in np.delete(
            solution[row_sec : row_sec + 3, col_sec : col_sec + 3].flatten(),
            (row_index - row_sec) * 3 + (column_index - col_sec),
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
    return sum([val.pop() * mult for val, mult in zip(solution_vals, multiplier)])


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


def solve_for_trivial_solutions(current_solutions, is_solved):
    total_no_soln = 0
    total_iters = 0

    while not is_solved:
        counter = total_iters % 3
        current_solutions, num_sol_found = find_trivial_solutions(
            current_solutions, subset_names[counter]
        )
        is_solved = is_completely_solved(current_solutions)

        if num_sol_found == 0:
            total_no_soln += 1

        if total_no_soln > 2:
            break

    return current_solutions, is_solved


def solve_for_preemptive_sets(current_solutions, is_solved):
    prev_num_sets_found = 1

    while not is_solved:
        current_solutions, num_sets_found = solve_preemptive_sets(current_solutions)

        is_solved = is_completely_solved(current_solutions)

        if prev_num_sets_found == num_sets_found:
            # print("Guessing required")
            # print(candidate_solutions)
            break

        prev_num_sets_found = num_sets_found

    return current_solutions, is_solved


def propagate_guess(previous_node, depth_of_guess):
    found_valid = False
    while not found_valid:
        for child in list(previous_node.children):
            if child.is_valid:
                depth_of_guess += 1
                previous_node = child
                target_row_index = child.index[0]
                target_col_index = child.index[1]
                target_solution = child.soln
                found_valid = True
                break

        if not found_valid:
            previous_node.is_valid = False
            previous_node.soln = None
            previous_node = previous_node.parent
            depth_of_guess -= 1

            if previous_node is None:
                break

    return (
        target_solution,
        target_row_index,
        target_col_index,
        found_valid,
        depth_of_guess,
        previous_node,
    )


def increment_guessing_index(row_index, col_index):
    col_index += 1
    if col_index == 9:
        row_index += 1
        col_index = 0

    return row_index, col_index


def is_guess_valid(current_solution, row_index, column_index, guess_val):
    fixed_vals = get_associated_vals(current_solution, row_index, column_index)

    if fixed_vals & {guess_val}:
        return False
    else:
        return True


def solve_using_guessing(current_solutions, is_solved):
    guess_depth = 0
    prev_node = AnyNode(guess_val=None, soln=current_solutions)
    # root = prev_node

    row_index = 0
    column_index = 0

    while row_index < 9 and column_index < 9 and not is_solved:
        cell_val = current_solutions[row_index, column_index]
        cell_len = len(cell_val)

        if cell_len == 1:
            row_index, column_index = increment_guessing_index(row_index, column_index)
            continue

        cell_val = list(cell_val)

        curr_solution = deepcopy(current_solutions)

        for val in cell_val:
            guess = deepcopy(curr_solution)

            if not is_guess_valid(guess, row_index, column_index, val):
                AnyNode(
                    parent=prev_node,
                    guess_val=val,
                    is_valid=False,
                    index=(row_index, column_index),
                )
                continue

            guess[row_index, column_index] = {val}

            try:
                temp = update_candidate_solutions(guess)
            except Exception:
                AnyNode(
                    parent=prev_node,
                    guess_val=val,
                    is_valid=False,
                    index=(row_index, column_index),
                )
                continue
            else:
                current_solutions = temp
                AnyNode(
                    parent=prev_node,
                    guess_val=val,
                    is_valid=True,
                    index=(row_index, column_index),
                    soln=temp,
                )

                is_solved = is_completely_solved(temp)

                if is_solved:
                    current_solutions = temp
                    found_valid = True
                    break

        (
            current_solutions,
            row_index,
            column_index,
            found_valid,
            guess_depth,
            prev_node,
        ) = propagate_guess(prev_node, guess_depth)

        is_solved = is_completely_solved(current_solutions)

        if not found_valid:
            # print(RenderTree(root))
            print("Invalid solution")
            break

    return current_solutions, is_solved


if __name__ == "__main__":

    input_file = os.path.join(".", "problem_96", "p096_sudoku.txt")

    all_puzzles = extract_puzzles_from_file(input_file)

    master_set = set(np.arange(1, 10))
    subset_names = ["square", "row", "column"]
    total_sum = 0

    store_puzzles_2 = dict()
    store_puzzles_2[6] = all_puzzles.get(6)

    for puzzle in all_puzzles.values():
        # for puzzle in store_puzzles_2.values():

        candidate_solutions = find_candidate_solutions(puzzle, master_set)

        total_no_soln = 0
        total_iters = 0

        solved = is_completely_solved(candidate_solutions)

        candidate_solutions, solved = solve_for_trivial_solutions(
            candidate_solutions, solved
        )

        if not solved:
            candidate_solutions = update_candidate_solutions(candidate_solutions)
            solved = is_completely_solved(candidate_solutions)
            candidate_solutions, solved = solve_for_preemptive_sets(
                candidate_solutions, solved
            )

        if not solved:
            candidate_solutions, solved = solve_using_guessing(candidate_solutions, solved)

        if solved:
            check_solution(candidate_solutions)
            puzzle_sum = puzzle_three_digit_num(candidate_solutions[0, 0:3])
            # print(puzzle_sum)
            total_sum += puzzle_sum

    print(f"Total sum: {total_sum}")
