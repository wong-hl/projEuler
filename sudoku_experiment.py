import numpy as np


def find_trivial_solutions(candidate_solutions, which_subset):
    print("\n")
    print(f"Solving for {which_subset} subset")
    for i in range(9):
        if which_subset == "square":
            row_index = (i//3)*3
            col_index = (i % 3)*3
            # print(f"row = {row_index} col = {col_index}")
            subset = candidate_solutions[row_index:row_index +
                                         3, col_index:col_index+3].flatten()
        elif which_subset == "row":
            subset = candidate_solutions[i, :]
        elif which_subset == "column":
            subset = candidate_solutions[:, i]

        print(subset)

        for index, _ in enumerate(subset):
            candidate = subset[index]
            if len(candidate) == 1:
                continue

            this_subset = np.delete(subset, index)
            vals_in_other_sets = [x & candidate for x in this_subset]
            if vals_in_other_sets:
                in_other_sets = set.union(*vals_in_other_sets)
                # print(f"in other sets {in_other_sets}")
                unique = candidate - set(in_other_sets)
                if unique:
                    print(f"{in_other_sets} {candidate}, {unique}")
                    # unique_val = min(unique)
                    # subset = [
                    #     adj_set - unique if unique_val in adj_set else adj_set for adj_set in subset]
                    subset[index] = unique
                    print(subset)
                    print()

        if which_subset == "square":
            candidate_solutions[row_index:row_index+3,
                                col_index:col_index+3] = np.asarray(subset).reshape(3, 3)
        elif which_subset == "row":
            candidate_solutions[i, :] = np.asarray(subset)
        elif which_subset == "column":
            candidate_solutions[:, i] = np.asarray(subset)

    candidate_solutions = update_candidate_solutions(candidate_solutions)

    return candidate_solutions

def update_candidate_solutions(candidate_solutions):
    for i in range(9):
        for j in range(9):
            cell_val = candidate_solutions[i, j]
            # print(f"i = {i} j= {j} val = {cell_val}")
            # print(cell_val)
            if len(cell_val) != 1:
                # print(cell_val)
                col_sec = (j // 3)*3
                row_sec = (i // 3)*3
                row = set().union(*[x for x in candidate_solutions[i, :] if len(x)==1])
                col = set().union(*[x for x in candidate_solutions[:, j] if len(x)==1])
                sector = set().union(*[x for x in candidate_solutions[row_sec:row_sec+3, col_sec:col_sec+3] if len(x) == 1])
                fixed_solutions = row | col | sector
                # print(cell_val & fixed_solutions)
                if cell_val & fixed_solutions: 
                    candidate_solutions[i, j] = cell_val - fixed_solutions

    return candidate_solutions

# Hardest (50)
# puzzle = np.asarray([[3, 0, 0, 2, 0, 0, 0, 0, 0],
# [0, 0, 0, 1, 0, 7, 0, 0, 0],
# [7, 0, 6, 0, 3, 0, 5, 0, 0],
# [0, 7, 0, 0, 0, 9, 0, 8, 0],
# [9, 0, 0, 0, 2, 0, 0, 0, 4],
# [0, 1, 0, 8, 0, 0, 0, 5, 0],
# [0, 0, 9, 0, 4, 0, 3, 0, 1],
# [0, 0, 0, 7, 0, 2, 0, 0, 0],
# [0, 0, 0, 0, 0, 8, 0, 0, 6]])

# Easiest (1)
puzzle = np.asarray([[0, 0, 3, 0, 2, 0, 6, 0, 0],
                     [9, 0, 0, 3, 0, 5, 0, 0, 1],
                     [0, 0, 1, 8, 0, 6, 4, 0, 0],
                     [0, 0, 8, 1, 0, 2, 9, 0, 0],
                     [7, 0, 0, 0, 0, 0, 0, 0, 8],
                     [0, 0, 6, 7, 0, 8, 2, 0, 0],
                     [0, 0, 2, 6, 0, 9, 5, 0, 0],
                     [8, 0, 0, 2, 0, 3, 0, 0, 9],
                     [0, 0, 5, 0, 1, 0, 3, 0, 0]])

candidate_solutions = np.empty((9, 9), dtype=set)
# print(len(candidate_solutions))

master_set = set(np.arange(1, 10))

for i in range(9):
    for j in range(9):
        cell_val = puzzle[i, j]
        # print(f"i = {i} j= {j} val = {cell_val}")
        # print(cell_val)
        if cell_val != 0:
            candidate_solutions[i, j] = {cell_val}
            # print(candidate_solutions[i, j])
        else:
            col_sec = (j // 3)*3
            row_sec = (i // 3)*3
            candidate_solutions[i, j] = master_set - (set(puzzle[i, :])
                                                      | set(puzzle[:, j]) |
                                                      set(puzzle[row_sec:row_sec+3, col_sec:col_sec+3].flatten()))
            # print(candidate_solutions[i, j])

print(candidate_solutions)


subset_names = ["square", "row", "column"]
target_cells = [1 for x in candidate_solutions[0, 0:3] if len(x) != 1]
total_iters = 0
counter = 0

while target_cells:
    counter = total_iters % 3
    candidate_solutions = find_trivial_solutions(candidate_solutions, subset_names[counter])
    target_cells = [1 for x in candidate_solutions[0, 0:3] if len(x) != 1]
    total_iters += 1

    if total_iters > 15:
        print("did not reach exit condidion")
        break

print(candidate_solutions)
