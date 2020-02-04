pairs = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4), (3, 4), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (0, 11), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11), (0, 12), (1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (11, 12)]


#                  0   1   2   3   4   5   6   7   8   9  10   1  12
rotate_indices = [12,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11]  # rotate clockwise
twist_indices  = [ 0, 12,  2,  3,  4,  8,  7,  6,  5,  9, 10, 11,  1]  # twist blue caps
flip_indices   = [ 0, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1]  # flip over

core = [True, True, False, False, False, True, True, True, True, False, False, False, True]  # true if blue


def calculate_inversion_set(numbers):
    # place-based definition, 0-based permutation assumed
    binary_vector = []
    for pair in pairs:
        binary_vector.append(
            numbers[pair[0]] > numbers[pair[1]]
        )
    return tuple(binary_vector)


# operations on a single vector

def rotate_vector_once(v):
    return [v[i] for i in rotate_indices]


def rotate(v, n):
    n = n % 13
    for i in range(n):
        v = rotate_vector_once(v)
    return v


def twist(v):
    is_colors = type(v[0]) == bool
    result = []
    for i in twist_indices:
        if is_colors and core[i]:
            result.append(not(v[i]))
        else:
            result.append(v[i])
    return result


def flip(v):
    is_colors = type(v[0]) == bool
    result = []
    for i in flip_indices:
        if is_colors:
            result.append(not(v[i]))
        else:
            result.append(v[i])
    return result


# processes

def find_best_rotation(numbers, colors):
    tuples = []

    for n in range(13):
        r_numbers, r_colors = rotate(numbers, n), rotate(colors, n)
        r_invnum = sum(calculate_inversion_set(r_numbers))
        tuples.append((r_invnum, r_numbers, r_colors, n))

    best_tuple = sorted(tuples)[0]
    return best_tuple[1::]  # numbers, colors, int:rotations


def find_best(numbers, colors):
    tuples = []
    f_numbers, f_colors = flip(numbers), flip(colors)

    for n in range(13):
        # rotated only
        r_numbers, r_colors = rotate(numbers, n), rotate(colors, n)
        r_invnum = sum(calculate_inversion_set(r_numbers))
        tuples.append((r_invnum, r_numbers, r_colors, n, False))
        # flipped after rotation
        fr_numbers, fr_colors = flip(r_numbers), flip(r_colors)
        fr_invnum = sum(calculate_inversion_set(fr_numbers))
        tuples.append((fr_invnum, fr_numbers, fr_colors, n, True))

    best_tuple = sorted(tuples)[0]
    return best_tuple[1::]  # numbers, colors, int:rotations, bool:flipped


def create_inversion_set_table(invset):
    invset_table = []
    for i in range(12):
        invset_row = []
        for j in range(i+1, 13):
            invset_index = pairs.index(tuple(sorted([i, j])))
            invset_element = invset[invset_index]
            invset_row.append(invset_element)
        invset_table.append(invset_row)
    return invset_table


def list_permutation_properties(numbers, colors):
    invset = calculate_inversion_set(numbers)
    return {
        'numbers': [item + 1 for item in numbers],
        'colors': colors,
        'yellow_sum': sum(colors),
        'inversion_set': create_inversion_set_table(invset),
        'inversion_number': sum(invset)
    }


def url_encode(numbers, colors):
    url_list = []
    for i in range(13):
        color = 'y' if colors[i] else 'w'
        number = str(numbers[i] + 1)  # 0-based calculation, 1-based output
        url_list.append(color + number)
    return ','.join(url_list)


def url_decode(url_str):
    url_list = url_str.split(',')
    numbers, colors = [], []
    for letter_number in url_list:
        colors.append(letter_number[0] == 'y')
        numbers.append(int(letter_number[1::]) - 1)  # 1-based input, 0-based calculation
    return numbers, colors

