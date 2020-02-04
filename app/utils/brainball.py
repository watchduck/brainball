from app.utils.peanuts import rotate, twist, flip, calculate_inversion_set, find_best_rotation, find_best, url_encode


class Brainball:

    def __init__(self, numbers, colors):
        self.numbers = numbers
        self.colors = colors

    def rotate(self, n):
        return Brainball(rotate(self.numbers, n), rotate(self.colors, n))

    def twist(self):
        return Brainball(twist(self.numbers), twist(self.colors))

    def flip(self):
        return Brainball(flip(self.numbers), flip(self.colors))

    def invset(self):
        return calculate_inversion_set(self.numbers)

    def invnum(self):
        return sum(self.invset())

    def best_rotation(self):
        # rotation with the lowest inversion number,
        # second return value is the number of rotations used
        numbers, colors, n = find_best_rotation(self.numbers, self.colors)
        return Brainball(numbers, colors), n

    def best(self):
        # position with the lowest inversion number,
        # other return values are the number of rotations used, and whether it was flipped
        numbers, colors, n, flipped = find_best(self.numbers, self.colors)
        return Brainball(numbers, colors), n, flipped

    def url_str(self):
        return url_encode(self.numbers, self.colors)
