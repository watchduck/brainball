from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from app.utils.peanuts import find_best, list_permutation_properties, url_encode, url_decode
from app.utils.list_related_permutations import list_related_permutations


def index_view(request):
    return render(request, 'app/index.html', {'range_13': range(13)})


def check_view(request):

    colors = []
    for i in range(13):
        post_index = 'color-{i}'.format(i=i)
        try:
            if request.POST[post_index]:
                colors.append(True)
        except KeyError:  # The checkbox is not checked, thus the key is not in the array.
            colors.append(False)

    numbers = []
    for i in range(13):
        post_index = 'number-{i}'.format(i=i)
        try:
            number = int(request.POST[post_index]) - 1  # 1-based input, 0-based calculation
            numbers.append(number)
        except ValueError:  # The passed string can not be converted to an integer.
            pass

    # go back to start page if input was not valid
    if not sorted(numbers) == list(range(13)):
        messages.error(request, "That was not a valid input!")
        return HttpResponseRedirect(reverse('index'))

    # otherwise find turned permutation with lowest inversion number
    numbers, colors, n, flipped = find_best(numbers, colors)

    if n > 0 or flipped:
        if n > 0 and flipped:
            message = "The entered position was turned right {n} times and then flipped over.".format(n=n)
        elif n > 0 and not flipped:
            message = "The entered position was turned right {n} times.".format(n=n)
        else:
            message = "The entered position was flipped over."
        messages.success(request, message)

    url_str = url_encode(numbers, colors)
    return HttpResponseRedirect(reverse('result', args=(url_str,)))


def result_view(request, url_str):
    numbers, colors = url_decode(url_str)
    twists, min_yellow_sum, min_inversion_number = list_related_permutations(numbers, colors)
    context = {
        'current': list_permutation_properties(numbers, colors),
        'twists': twists,
        'min_yellow_sum': min_yellow_sum,
        'min_inversion_number': min_inversion_number,
        'numbers_0_12': range(13)
    }
    return render(request, 'app/result.html', context)
