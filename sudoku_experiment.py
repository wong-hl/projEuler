from typing_extensions import ParamSpec
import numpy as np
from copy import deepcopy
from anytree import AnyNode, Node, RenderTree


def find_trivial_solutions(candidate_solutions, which_subset):

    num_solns = 0

    for i in range(9):
        if which_subset == "square":
            row_index = (i//3)*3
            col_index = (i % 3)*3

            subset = candidate_solutions[row_index:row_index +
                                         3, col_index:col_index+3].flatten()
        elif which_subset == "row":
            subset = candidate_solutions[i, :]
        elif which_subset == "column":
            subset = candidate_solutions[:, i]

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
            candidate_solutions[row_index:row_index+3,
                                col_index:col_index+3] = np.asarray(subset).reshape(3, 3)
        elif which_subset == "row":
            candidate_solutions[i, :] = np.asarray(subset)
        elif which_subset == "column":
            candidate_solutions[:, i] = np.asarray(subset)

    candidate_solutions = update_candidate_solutions(candidate_solutions)

    return candidate_solutions, num_solns


def update_candidate_solutions(candidate_solutions):
    for i in range(9):
        for j in range(9):

            cell_val = candidate_solutions[i, j]

            if len(cell_val) != 1:
                col_sec = (j // 3)*3
                row_sec = (i // 3)*3

                row = set.union(
                    *[x for x in candidate_solutions[i, :] if len(x) == 1])
                col = set.union(
                    *[x for x in candidate_solutions[:, j] if len(x) == 1])
                sector = set.union(
                    *[x for x in candidate_solutions[row_sec:row_sec+3, col_sec:col_sec+3].flatten() if len(x) == 1])

                fixed_solutions = row | col | sector

                if cell_val & fixed_solutions:
                    difference = cell_val - fixed_solutions
                    if difference:
                        candidate_solutions[i, j] = difference
                    else:
                        raise Exception("Invalid solution present")

    return candidate_solutions


def update_subset_preemptive(mask, candidate_set_subset, preemptive_set):
    # print(
    #     f"target set: {preemptive_set}\n mask: {mask}\n candidateset: {candidate_set_subset}\n")

    # for counter, in_set in enumerate(mask):
    #     val = candidate_set_subset[counter]
    #     if not in_set and len(val) != 1:
    #         candidate_set_subset[counter] = val - (val & preemptive_set)

    # # updated_vals = [val - (val & preemptive_set) if len(val) != 1 and not in_set else val for val, in_set in zip(candidate_set_subset, mask)]
    # updated_vals = [val - (val & preemptive_set) if len(val) != 1 and not in_set else val for val, in_set in zip(candidate_set_subset, mask)]

    # print(candidate_set_subset)
    # print()
    return np.asarray([val - (val & preemptive_set) if len(val) != 1 and not in_set else val for val, in_set in zip(candidate_set_subset, mask)])


def solve_preemptive_sets(candidate_solutions):
    num_sets_found = 0
    for i in range(9):
        for j in range(9):
            col_sec = (j // 3)*3
            row_sec = (i // 3)*3

            cell_val = candidate_solutions[i, j]
            cell_len = len(cell_val)

            if cell_len == 1:
                continue

            row_mask = candidate_solutions[i, :] <= cell_val
            col_mask = candidate_solutions[:, j] <= cell_val
            sector_mask = candidate_solutions[row_sec:row_sec +
                                              3, col_sec:col_sec+3] <= cell_val

            if row_mask.sum() == cell_len:
                candidate_solutions[i, :] = update_subset_preemptive(
                    row_mask, candidate_solutions[i, :], cell_val)
                num_sets_found += 1

            if col_mask.sum() == cell_len:
                candidate_solutions[:, j] = update_subset_preemptive(
                    col_mask, candidate_solutions[:, j], cell_val)
                num_sets_found += 1

            if sector_mask.sum() == cell_len:
                sector = candidate_solutions[row_sec:row_sec +
                                             3, col_sec:col_sec+3].flatten()
                sector_mask = sector_mask.flatten()
                candidate_solutions[row_sec:row_sec+3, col_sec:col_sec+3] = update_subset_preemptive(
                    sector_mask, sector, cell_val).reshape((3, 3))
                num_sets_found += 1

    candidate_solutions = update_candidate_solutions(candidate_solutions)

    return candidate_solutions, num_sets_found


def is_completely_solved(candidate_solutions):
    length_checker = np.vectorize(len)
    what_lengths = length_checker(candidate_solutions) == 1
    if what_lengths.sum() == 81:
        return True
    else:
        return False


def is_sufficiently_solved(candidate_solutions):
    target_cells = [1 for x in candidate_solutions[0, 0:3] if len(x) != 1]
    if target_cells:
        return False
    else:
        return True


def first_guess(candidate_solutions):
    for i in range(9):
        for j in range(9):
            if len(candidate_solutions[i, j]) != 1:
                return candidate_solutions[i, j], i, j

# class Node:
#     def __init__(self, value):
#         self.value = value


# class GuessingTree:
#     def __init__(self):
#         self.index = index
#         self.is_violation = is_violation
#         self.children = []
#         if children is not None:
#             for child in children:
#                 self.add_child(child)

#     def __repr__(self):
#         return f"Name: {self.name}, Index: {self.index}"

#     def add_child(self, node):
#         assert isinstance(node, GuessingTree)
#         self.children.append(node)

# Hardest (50)
puzzle = np.asarray([[3, 0, 0, 2, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0, 7, 0, 0, 0],
                     [7, 0, 6, 0, 3, 0, 5, 0, 0],
                     [0, 7, 0, 0, 0, 9, 0, 8, 0],
                     [9, 0, 0, 0, 2, 0, 0, 0, 4],
                     [0, 1, 0, 8, 0, 0, 0, 5, 0],
                     [0, 0, 9, 0, 4, 0, 3, 0, 1],
                     [0, 0, 0, 7, 0, 2, 0, 0, 0],
                     [0, 0, 0, 0, 0, 8, 0, 0, 6]])

# Easiest (1)
# puzzle = np.asarray([[0, 0, 3, 0, 2, 0, 6, 0, 0],
#                      [9, 0, 0, 3, 0, 5, 0, 0, 1],
#                      [0, 0, 1, 8, 0, 6, 4, 0, 0],
#                      [0, 0, 8, 1, 0, 2, 9, 0, 0],
#                      [7, 0, 0, 0, 0, 0, 0, 0, 8],
#                      [0, 0, 6, 7, 0, 8, 2, 0, 0],
#                      [0, 0, 2, 6, 0, 9, 5, 0, 0],
#                      [8, 0, 0, 2, 0, 3, 0, 0, 9],
#                      [0, 0, 5, 0, 1, 0, 3, 0, 0]])

candidate_solutions = np.empty((9, 9), dtype=set)
# print(len(candidate_solutions))

master_set = set(np.arange(1, 10))

for i in range(9):
    row_val = puzzle[i, :]
    row_set = set(row_val)
    for j in range(9):

        cell_val = puzzle[i, j]

        if cell_val != 0:
            candidate_solutions[i, j] = {cell_val}
        else:
            col_sec = (j // 3)*3
            row_sec = (i // 3)*3
            candidate_solutions[i, j] = master_set - (row_set | set(puzzle[:, j]) |
                                                      set(puzzle[row_sec:row_sec+3, col_sec:col_sec+3].flatten()))

print(candidate_solutions)


subset_names = ["square", "row", "column"]
total_no_soln = 0
total_iters = 0

solved = is_sufficiently_solved(candidate_solutions)

while not solved:
    counter = total_iters % 3
    candidate_solutions, num_sol_found = find_trivial_solutions(
        candidate_solutions, subset_names[counter])
    solved = is_sufficiently_solved(candidate_solutions)

    if num_sol_found == 0:
        total_no_soln += 1
        print(total_iters)

    if total_no_soln > 2:
        print("No trivial solution found")
        break

if solved:
    print("\nSolved using trivial method")
    print(candidate_solutions)

if not solved:
    print()
    candidate_solutions = update_candidate_solutions(candidate_solutions)
    solved = is_sufficiently_solved(candidate_solutions)
    prev_num_sets_found = 1

    while not solved:
        candidate_solutions, num_sets_found = solve_preemptive_sets(
            candidate_solutions)

        solved = is_completely_solved(candidate_solutions)

        if prev_num_sets_found == num_sets_found:
            print("Guessing required")
            break

        prev_num_sets_found = num_sets_found

    print(candidate_solutions)

# if not solved:
#     row = candidate_solutions[0, :]
#     block = candidate_solutions[0:3, 0:3]
#     for i in range(3):
#         target_cell = candidate_solutions[0, i]
#         if len(target_cell) != 1:
#             col = candidate_solutions[i, :]
#             target_cell = list(target_cell)
#             for val in target_cell:
#                 print(val)
#                 candidate_solutions[0,i] = {val}
#                 try:
#                     temp = update_candidate_solutions(candidate_solutions)
#                     print(temp)
#                 except Exception:
#                     continue

#                 candidate_solutions = temp
#                 break


#     print("guess")

# if not solved:
#     guess_depth = 0
#     name = str(guess_depth)
#     # guesses = Node(str(guess_depth), guess_val = None)
#     prev_node = AnyNode(id = str(guess_depth), guess_val = None)
#     root = prev_node
#     prev_name = name

#     i = 0
#     j = 0

#     while i < 9 and j < 9:
#         # for j in range(9):
#         else_reached = False

#         cell_val = candidate_solutions[i, j]
#         cell_len = len(cell_val)
#         print(f"{i} {j} {cell_val}")

#         if cell_len == 1:
#             j += 1
#             if j == 9:
#                 i += 1
#                 j = 0
#             continue

#         cell_val = list(cell_val)

#         for index, val in enumerate(cell_val):
#             guess = deepcopy(candidate_solutions)
#             guess[i, j] = {val}
#             try:
#                 temp = update_candidate_solutions(guess)
#             except Exception:
#                 name = f"{guess_depth + 1}_{index}"
#                 this_node = AnyNode(id=name,
#                         parent=prev_node, guess_val=val, is_valid = False, index = (i,j))
#                 continue
#             else:
#                 candidate_solutions = temp
#                 else_reached = True
#                 name = f"{guess_depth + 1}_{index}"
#                 this_node = AnyNode(id=name,
#                         parent=prev_node, guess_val=val, is_valid = True, index = (i,j), soln = temp)
#                 # prev_name = name
#                 # prev_node = this_node
#                 # print(candidate_solutions)
#                 # break

#         print(prev_node)

#         found_valid = False
#         for child in list(prev_node.children):
#             print(child.is_valid)
#             if child.is_valid:
#                 guess_depth += 1
#                 prev_name = child.id
#                 prev_node = child
#                 i = child.index[0]
#                 j = child.index[1]
#                 candidate_solutions = child.soln
#                 found_valid = True

#         if not found_valid:
#             print("Invalid solution")
#             break

#         # guess_depth += 1
#         # prev_name = name
#         # prev_node = this_node
#         # j += 1
#         # if j == 9:
#         #     j = 0
#         #     i += 1


#        # print(RenderTree(root))
    # print(RenderTree(root))

#         # break
#     # row = candidate_solutions[0, :]
#     # block = candidate_solutions[0:3, 0:3]
#     # for i in range(3):
#     #     target_cell = candidate_solutions[0, i]
#     #     if len(target_cell) != 1:
#     #         col = candidate_solutions[i, :]
#     #         target_cell = list(target_cell)
#     #         for val in target_cell:
#     #             print(val)
#     #             candidate_solutions[0,i] = {val}
#     #             try:
#     #                 temp = update_candidate_solutions(candidate_solutions)
#     #                 print(temp)
#     #             except Exception:
#     #                 continue

#     #             candidate_solutions = temp
#     #             break


# print(candidate_solutions)
