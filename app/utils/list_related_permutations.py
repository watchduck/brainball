from app.utils.brainball import Brainball
from app.utils.peanuts import rotate, create_inversion_set_table, core


def list_related_permutations(numbers, colors):
    current = Brainball(numbers, colors)
    twists = []

    yellow_sums = []
    inversion_numbers = []

    for n in range(13):
        r1 = current.rotate(n)
        r2 = r1.flip()

        tr1 = r1.twist()
        tr2 = r2.twist()

        best_tr1, n1 = tr1.best_rotation()
        best_tr2, n2 = tr2.best_rotation()

        adapted_r1 = r1.rotate(n1)
        adapted_r2 = r2.rotate(n2)

        adapted_core1 = rotate(core, n1)
        adapted_core2 = rotate(core, n2)

        twists.append([
            {
                'before_numbers': [item+1 for item in adapted_r1.numbers],
                'before_colors': adapted_r1.colors,
                'core': adapted_core1,
                'numbers': [item+1 for item in best_tr1.numbers],
                'colors': best_tr1.colors,
                'yellow_sum': sum(best_tr1.colors),
                'inversion_set': create_inversion_set_table(best_tr1.invset()),
                'inversion_number': best_tr1.invnum(),
                'url': '/' + best_tr1.url_str()
            },
            {
                'before_numbers': [item+1 for item in adapted_r2.numbers],
                'before_colors': adapted_r2.colors,
                'core': adapted_core2,
                'numbers': [item+1 for item in best_tr2.numbers],
                'colors': best_tr2.colors,
                'yellow_sum': sum(best_tr2.colors),
                'inversion_set': create_inversion_set_table(best_tr2.invset()),
                'inversion_number': best_tr2.invnum(),
                'url': '/' + best_tr2.url_str()
            },
        ])

        yellow_sums += [sum(best_tr1.colors), sum(best_tr2.colors)]
        inversion_numbers += [best_tr1.invnum(), best_tr2.invnum()]

    min_yellow_sum = min(yellow_sums)
    min_inversion_number = min(inversion_numbers)

    for twist_pair in twists:
        for twist in twist_pair:
            twist['yellow_sum_minimal'] = twist['yellow_sum'] == min_yellow_sum
            twist['inversion_number_minimal'] = twist['inversion_number'] == min_inversion_number

    return twists, min_yellow_sum, min_inversion_number
